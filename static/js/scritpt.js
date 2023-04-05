
async function zoomin(){
    let inputs = JSON.parse(localStorage.getItem('inputs'));
    const res = await fetch(window.location.pathname,{method:'POST',body:{...inputs,task:"zoom-in",maxZoom:"false"},
    headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
    console.log(res);
}


const submit_button = document.querySelector('#submit-button')

submit_button.addEventListener('click',(e)=>{
    let inputs = Object.create(null)
    const form = e.target.form

    for(let i in form){
        if(/^\d+$/.test(i) && form[i].name!=""){
            inputs[form[i].name] = form[i].value
        }
        else break;
    }
    console.log(inputs)
    localStorage.setItem('inputs',JSON.stringify(inputs))
})

const graph = document.querySelector('.graph-plot')
