/*------------------------------更改姓名----------------------------*/
let result
let updatebtn=document.getElementById("update");
const changeNameapi="http://127.0.0.1:3000/api/user"
updatebtn.addEventListener("click", ()=>{
    let nameinput=document.getElementById("name").value;
    if (nameinput){
        fetch(changeNameapi, {
            method:"POST",
            headers:{
                "Content-Type": "application/json"
            },
            body:JSON.stringify({"name":nameinput})
        }).then((response)=>{
            return response.json();
        }).then((result)=>{
            if (result["null"]){
                alert("請輸入欲更改名稱!");
            } else {
                changeName(result, nameinput);
            }
        })
    } else {
        alert("請輸入欲更改名稱!");
    }
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