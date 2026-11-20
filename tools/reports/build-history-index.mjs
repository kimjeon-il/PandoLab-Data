// Generate the searchable history catalog from three canonical report kinds.
// No dependencies, network, GIS conversion or application writes.
import {readdir, readFile, writeFile} from "node:fs/promises";
import {join, relative, resolve} from "node:path";
import {fileURLToPath} from "node:url";
const root=resolve(fileURLToPath(new URL("../..",import.meta.url)));
const reports=join(root,"reports");
const dirs=["history/countries","history/decades","history/geography"];
async function collect(dir){
  let result=[];
  for(const item of await readdir(dir,{withFileTypes:true})){
    const target=join(dir,item.name);
    if(item.isDirectory())result.push(...await collect(target));
    else if(item.isFile()&&item.name.endsWith(".json"))result.push(target);
  }
  return result;
}
const records=[];
for(const dir of dirs){
 const expectedType=dir==="history/countries"?"entity":dir==="history/decades"?"event":"geography";
 let entries=[];
 try{entries=await collect(join(reports,dir))}catch(e){if(e.code!=="ENOENT")throw e}
 for(const filename of entries){
   const value=JSON.parse(await readFile(filename,"utf8"));
   if(value.schema!=="pando-history-report-v1")continue;
   if(value.type!==expectedType)throw new Error(`Invalid type in ${filename}: expected ${expectedType}`);
   if(value.type==="event"){
     const year=value.date?.year;
     if(year!==null&&(!Number.isInteger(year)||year<1801))throw new Error(`Invalid year: ${filename}`);
     const decade=year===null?"undated":`${Math.floor(year/10)*10}-${Math.floor(year/10)*10+9}`;
     const folder=relative(join(reports,dir),filename).replaceAll("\\","/").split("/")[0];
     if(folder!==decade)throw new Error(`Event in wrong decade: ${filename}`);
   }
   const path=relative(root,filename).replaceAll("\\","/");
   records.push({
     id:value.id,type:value.type,path,title:value.title,
     entityKeys:value.type==="entity"?[value.subject.key]:(value.entityKeys??[]),
     eventIds:value.type==="entity"?(value.eventIds??[]):[],
     year:value.type==="event"?(value.date?.year??null):null,
     research:value.status.research,application:value.status.application
   });
 }
}
records.sort((a,b)=>a.id.localeCompare(b.id,"en"));
const byYear={},byEntity={},byType={entity:[],event:[],geography:[]};
for(const r of records){
 byType[r.type].push(r.id);
 if(r.type==="event"){
   const year=r.year===null?"undated":String(r.year);
   (byYear[year]??=[]).push(r.id);
 }
 for(const key of r.entityKeys)(byEntity[key]??=[]).push(r.id);
}
// Chronological navigation is a derived view: never duplicate event reports by decade.
const decadeOf=year=>{
  if(!Number.isInteger(year)||year<1801)return null;
  const start=Math.floor(year/10)*10;
  return `${start}-${start+9}`;
};
const byDecade={};
for(const record of records){
  if(record.type!=="event")continue;
  const decade=decadeOf(record.year);
  if(decade)(byDecade[decade]??=[]).push(record.id);
}
const orderDecades=groups=>Object.fromEntries(
  Object.entries(groups).sort(([a],[b])=>a.localeCompare(b,"en"))
);
const recordById=new Map(records.map(record=>[record.id,record]));
const byCountry={};
for(const [key,recordIds] of Object.entries(byEntity).sort(([a],[b])=>a.localeCompare(b,"en"))){
  if(!/^(?:state:|dependency:|research:(?:state|dependency):)/.test(key))continue;
  const decades={};
  for(const id of recordIds){
    const record=recordById.get(id);
    if(record.type!=="event")continue;
    const decade=decadeOf(record.year);
    if(decade)(decades[decade]??=[]).push(id);
  }
  byCountry[key]={recordIds,byDecade:orderDecades(decades)};
}
const output={schema:"pando-history-catalog-v1",generatedFrom:dirs,entries:records,byType,byEntity,byYear,byDecade:orderDecades(byDecade),byCountry};
await writeFile(join(reports,"history","catalog.json"),JSON.stringify(output,null,2)+"\n");
