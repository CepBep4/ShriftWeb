class StateApp{
    constructor(){
        this.focusId = undefined;
    }
};

//Виджет слоя
class Lays{
    constructor(){
        this.obj=undefined
        this.elements=[]
    }

    createWidgets(id, name){
        let element=`
        <div class="lay-${id}" id="lay-${id}" onclick="focusLayer(${id});"> ${name}
            <div id="l-${id}-b${id}" onclick="lays.removeWidgets(${id});"></div>
        </div>
        <style>
            #lay-${id}{
                border-radius: 10px;
                width: 14%;
                font-family: 'Cygre';
                font-size: 21px;
                background: gray;
                position: relative;
                left: 10px;
                top: 10px;
                display: block;
                margin-bottom: 10px;
                transition: all 0.2s
            }
            
            #l-${id}-b${id}{
                width: 20px;
                height: 20px;
                border-radius: 180px;
                background: red;
                border: 0px;
                display: inline-block;
                float: right;
                translate: -3px 1px;
            }        
        </style> 
        `;  
        this.elements.push(element)
        document.getElementById('lays-place')
        .innerHTML=this.elements.join(); 
    }

    updateWidgets(){
        document.getElementById('lays-place')
        .innerHTML=this.elements.join();        
    }

    removeWidgets(id){
        delete this.elements[id];
        fetch(`${HOST}/setcoockie`,{
            method: "POST",
            body: JSON.stringify({
                delete: 'element',
                id: id 
                })
            });
        refresh();
    }

}

const HOST = "http://127.0.0.1:5000";
var check = false;
var lays = new Lays();
var stateApp= new StateApp();
const maxEffect=3;

function refresh(){
    location.reload();
};

function getCookie(){
    fetch(`${HOST}/getcoockie`,
    {method: "GET"})
    .then(resp => resp.text())
    .then(session => {
        session=JSON.parse(session);
        if(session['project_width']){
            document.getElementById('input-real-width').value=session['project_width']
            document.getElementById('input-real-height').value=session['project_height']
        }
        if(!session['user_id']){
            fetch(`${HOST}/logout`, {method: "GET"});
            location.reload();            
        }
        if (session['element']){
            for(let i = 0; i<=maxEffect; i++){
                if(session['element'][i]!=undefined){
                    lays.createWidgets(i, session['element'][i])
                }
                else{
                    break
                }
            }
        }
        if (session['element'][0]){
            document.getElementById('prewiew-image').src=`../static/projects/${session['user_id']}.jpg`;
        }
    });
}

function checkOnLoad(){
    getCookie();
    lays.updateWidgets()
    changeFocusLayer();
}

function checkInputSize(){
    width=document.getElementById('input-real-width');
    height=document.getElementById('input-real-height');

    if(width.value>30){width.value=30}
    else if(width.value<1){width.value=1}
    if(height.value>30){height.value=30}
    else if(height.value<1){height.value=1}
}

function changeSizeProject(){
    loadIcon();
    realWidth=document.getElementById('input-real-width').value;
    realHeight=document.getElementById('input-real-height').value;
    if (realHeight=='' | realWidth==''){
        alert('Укажите размеры проекта!');
        return 0;
    }
    fetch(`${HOST}/setcoockie`,{
        method: "POST",
        body: JSON.stringify({
            project_width: realWidth,
            project_height: realHeight 
            })
        });
        
        setTimeout(() => {
            fetch(`${HOST}/getlayout`,{method: "POST",
                body: JSON.stringify({
                    project_width: realWidth,
                    project_height: realHeight 
            })})
            .then(resp => resp.text())
            .then(answer => {
                user_id=answer;
                document.getElementById('prewiew-image').src=`../static/projects/${user_id}.jpg`;
                refresh();
            });

        }, 500)
        // document.getElementById('loads').style.opacity=0;
        // document.getElementById('loads').style.visibility='hidden';
        // document.getElementsByClassName('loader').style.opacity=0;
        // document.getElementsByClassName('loader').style.visibility='hidden';
         

    
}

function focusLayer(id){
    if (stateApp.focusId!=id){
        stateApp.focusId=id;
        document.getElementById(`lay-${id}`).style.background='#62ffa4';
        if(lays.elements.length>1){
            for(let i=0; i<=lays.elements.length; i++){
                if(i!=id){
                    // try {document.getElementById(`lay-${i}`).style.background='gray'}catch(error){}
                    document.getElementById(`lay-${i}`).style.background='gray'
                }
            }
        }

    }
    else{
        stateApp.focusId=undefined;
        document.getElementById(`lay-${id}`).style.background='gray';
    }
    changeFocusLayer();
}

function changeFocusLayer(){
    if(stateApp.focusId==undefined){
        document.getElementById('default-layer').style.visibility='visible'
        document.getElementById('main-layer').style.visibility='hidden'
        document.getElementById('choice-next-layer').style.visibility='hidden'
    }
    else{
        document.getElementById('default-layer').style.visibility='hidden'
        document.getElementById('main-layer').style.visibility='hidden'
        document.getElementById('choice-next-layer').style.visibility='hidden'
    }
    if(stateApp.focusId==0){
        document.getElementById('choice-next-layer').style.visibility='hidden'
        document.getElementById('main-layer').style.visibility='visible'
        document.getElementById('default-layer').style.visibility='hidden'
        
    }
}

function loadIcon(){
    document.getElementById('loads').style.visibility='visible';
    document.getElementById('loads').style.opacity=1;
    document.getElementById('loader').style.visibility='visible';
    document.getElementById('loader').style.opacity=1;
}

function addEffect(){
    document.getElementById('choice-next-layer').style.visibility='visible'
    document.getElementById('choice-next-layer').style.visibility='visible'
    document.getElementById('choice-next-layer').style.visibility='visible'
    document.getElementById('choice-next-layer').style.visibility='visible'
    document.getElementById('choice-next-layer').style.visibility='visible'
    document.getElementById('default-layer').style.visibility='hidden'
    document.getElementById('main-layer').style.visibility='hidden'    
}

function addShrift(){
    loadIcon();
    fetch(`${HOST}/addshrift`,{
        method: "POST",
        body: JSON.stringify({
            project_width: 1,
            project_height: 1 
            })
        });
        setTimeout(() => {refresh();}, 500)
}
