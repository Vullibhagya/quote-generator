async function getQuote(){

    const response=await fetch("/quote");

    const data=await response.json();

    document.getElementById("quoteBox").innerHTML=`
        <h3>${data.quote}</h3>
        <p>- ${data.author}</p>
    `;

    loadHistory();
}

async function loadHistory(){

    const response=await fetch("/history");

    const history=await response.json();

    const div=document.getElementById("history");

    div.innerHTML="";

    history.forEach(item=>{

        div.innerHTML+=`
        <div class="history-item">
            <b>${item.quote}</b><br>
            <i>${item.author}</i>
        </div>
        `;
    });

}

loadHistory();