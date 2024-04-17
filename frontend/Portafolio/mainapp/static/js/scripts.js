const defaultFile = 'http://127.0.0.1:8000/media/blank_profile.png'

const file = document.getElementById('foto');
const img = document.getElementById('img');


file.addEventListener( 'change', e =>{

    if(e.target.files[0]){
        const reader = new FileReader();
        reader.onload = function(e){
            img.src = e.target.result;
        }
        reader.readAsDataURL(e.target.files[0])
    }else{
        img.src = defaultFile
    }
});

