const container = document.getElementById('botonprueba');


function addInput(){
    let input = document.createElement('input');
    input.placeholder = 'Type something';
    container.appendChild(input);
}