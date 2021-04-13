/*------------------------------帳號查姓名----------------------------*/
let dataset;
let querybtn=document.getElementById("search");
querybtn.addEventListener("click", ()=>{
    let searchinput=document.getElementById("username").value;
    if (searchinput){
        let url="http://127.0.0.1:3000/api/users?username="+searchinput;
        fetch(url).then((response)=>{
            return response.json()
        }).then((dataset)=>{
            if (dataset.data === "null"){
                noMatch(searchinput);
            } else if (dataset.data === "Need data input!") {
                alert("請輸入查詢資料!");
            } else {
                oneMatch(dataset.data);
            }
        })
    } else {
        alert("請輸入查詢資料!");
    }    
})
oneMatch=(datas)=>{
    const resultname=datas["name"]
    const resultaccount=datas["username"]
    let showresult=document.createElement("div");
    showresult.textContent=resultname+"("+resultaccount+")";
    showresult.id="searchresult";
    let parent=document.querySelector(".querypart");
    let oldnode=document.getElementById("searchresult");
    if (oldnode){
        parent.replaceChild(showresult, oldnode);
    } else {
        oldnode=document.getElementById("forinsert");
        parent.insertBefore(showresult, oldnode);
    }
}
noMatch=(name)=>{
    let showresult=document.createElement("div");
    showresult.textContent="null"+"("+name+")";
    showresult.id="searchresult";
    let parent=document.querySelector(".querypart");
    let oldnode=document.getElementById("searchresult");
    if (oldnode){
        parent.replaceChild(showresult, oldnode);
    } else {
        oldnode=document.getElementById("forinsert");
        parent.insertBefore(showresult, oldnode);
    }
}