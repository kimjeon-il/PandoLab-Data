// Generate the searchable history catalog from three canonical report kinds.
// No dependencies, network, GIS conversion or application writes.
import {readdir, readFile, writeFile} from "node:fs/promises";
import {join, relative, resolve} from "node:path";
import {fileURLToPath} from "node:url";
const root=resolve(fileURLToPath(new URL("../..",import.meta.url)));
const reports=join(root,"reports");
const dirs=["entities","events","geography"];
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
 let entries=[];
 try{entries=await collect(join(reports,dir))}catch(e){if(e.code!=="ENOENT")throw e}
 for(const filename of entries){
   const value=JSON.parse(await readFile(filename,"utf8"));
   if(value.schema!=="pando-history-report-v1")continue;
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
const output={schema:"pando-history-catalog-v1",generatedFrom:dirs,entries:records,byType,byEntity,byYear};
await writeFile(join(reports,"research","catalog.json"),JSON.stringify(output,null,2)+"\n");
