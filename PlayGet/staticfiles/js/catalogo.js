const input = document.getElementById('hidden-input')

function checkboxes_fun(element, tipo) {
    if (element.checked) {
        input.value += element.name+";"
        console.log('Checking: '+ input.value)
    } else {
        input.value = input.value.replaceAll(element.name+';','')
        console.log('Unchecking: '+ input.value)
    }
}
