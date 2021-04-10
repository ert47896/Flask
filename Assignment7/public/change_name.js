/*------------------------------更改姓名----------------------------*/
let updatebtn=document.getElementById("update");
const changeNameapi="http://127.0.0.1:3000/api/user"
updatebtn.addEventListener("click", ()=>{
    let nameinput=document.getElementById("name").value;
    fetch(changeNameapi, {
        method:"POST",
        headers:{
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"name":nameinput})
    }).then((response)=>{
        return response.json();
    }).then((resultData)=>{
        changeName(resultData, nameinput);
    })
    // let req=new XMLHttpRequest();
    // req.open("POST", "http://127.0.0.1:3000/api/user");
    // req.setRequestHeader("Content-Type", "application/json");
    // req.onload=()=>{
    //     result=JSON.parse(req.responseText);
    //     changeName(result, nameinput);
    // }
    // req.send(JSON.stringify({"name":nameinput}));
})
changeName=(status, nextname)=>{
    let mainnode=document.querySelector(".querypart");
    let showstatus=document.createElement("div");
    showstatus.id="updatestatus";
    let oldnode=document.getElementById("updatestatus");
    if (status["ok"]){
        let oldname=document.getElementById("myname");
        let newname=document.createElement("span");
        newname.textContent=nextname;
        newname.id="myname";
        let parent=document.getElementById("forchange");
        parent.replaceChild(newname, oldname);
        showstatus.textContent="更新成功";                
        if (oldnode){
            mainnode.replaceChild(showstatus, oldnode);
        } else {
            mainnode.appendChild(showstatus);
        }
    } else {
        showstatus.textContent="更新失敗";
        if (oldnode){
            mainnode.replaceChild(showstatus, oldnode);
        } else {
            mainnode.appendChild(showstatus);
        }
    }
}