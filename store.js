var removeCardItemButtons = document.getElementById('btn-danger')
console.log(removeCardItemButtons)
for(var i=0; i< removeCardItemButtons.length;i++){
    var button = removeCardItemButtons[i]
    button.addEventListener('click', function(event){
        console.log('clicked')
    })
}