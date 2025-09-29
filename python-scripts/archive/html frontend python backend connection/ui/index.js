async function getDataFromPython() {
    document.getElementById('myele').innerText = await Element.get_data()();
}

document.getElementById('mybtn').addEventListener('click', () => {
    getDataFromPython();
});

document.getElementById('sendbtn').addEventListener('click', async () => {
    await Element.send_data('Hello from JS');
});