

//Загружается поумолчанию
function onload() { 
    login = document.getElementById('login');
    password = document.getElementById('password');
}

//Кнопка войти
function loginEnter(){
    const HOST = "http://127.0.0.1:5000"
    if(login.value!="" & password.value!=""){
        fetch(`${HOST}/login`,{
        method: "POST",
        body: JSON.stringify({
            login: login.value,
            password: password.value 
            })
        })
        .then(resp => resp.text())
        .then(answer => {
            if(answer=='False'){
                let login_label = document.getElementById('label-input-data');
                let login = document.getElementById('login');
                let password = document.getElementById('password');
                let sqframe = document.getElementById('reqtangle-login-pass');
                let pixels = 30

                login_label.innerHTML='Неверный логин или пароль';
                login_label.style.color='white';
                login_label.style.borderColor='red';

                sqframe.style.background="red";
                sqframe.style.translate='-30px';
                setTimeout(() => {sqframe.style.translate='30px';}, 100)
                setTimeout(() => {sqframe.style.translate='0px';}, 200)
                setTimeout(() => {sqframe.style.opacity=0;}, 450)
                setTimeout(() =>
                {
                    login_label.innerHTML='Введите свои данные';
                    login_label.style.color='black';
                    login_label.style.borderColor='black';
                    sqframe.style.background="linear-gradient(white, #2e2caa46 80%)";
                    login.value="";
                    password.value="";
                },1000)
                setTimeout(() => {sqframe.style.opacity=1;}, 1000)

                // setTimeout(() => location.reload(), 600)
                
            }
            else{
                location.reload();
            };
        });
    }
    else {
        if(login.value=="" & password.value!=""){
            alert('Введите логин');
        }
        else if(password.value=="" & login.value!=""){
            alert('Введите пароль');
        }
        else {
            alert('Введите логин и пароль');
        };
    };
};

function LoginExit(){
    const HOST = "http://127.0.0.1:5000"
    fetch(`${HOST}/logout`, {method: "GET"});
    location.reload();
};