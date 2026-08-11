function status(){return request({url:"/api/status",method:"get",timeout:2000})}
function list(params){return request({url:"/api/docker/containers",method:"get",params:{all:params.all,includeStats:params.stats}})}
function start(id){return request({url:`/api/docker/containers/${id}/start`,method:"post"})}
function update(key,data){return request({url:"/api/ddns/task/"+key,method:"put",data:data})}
const socketPath="/api/status/ws";
