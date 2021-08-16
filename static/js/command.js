console.log('Hello world')

var updatePresent = document.getElementsByClassName('update-presence')

for (i = 0; i < updatePresent.length; i++) {
    updatePresent[i].addEventListener('click', function(){
        var crewId = this.dataset.crewid
        var presence = this.dataset.presence
        console.log('CrewId:', crewId, 'Presence:', presence)

        updateAttendance(crewId, presence)
        // console.log('USER:', user)
        // if(user === 'AnonymousUser'){
        // }else{
        //     updateUserOrder(crewId, present)
        // }
    })
}

// function  checkAttendance(crewId, present){
//     console.log('CrewId: ', crewId)
//     console.log('Presence: ', present)
//     if (present == 'checked'){
//         crew = Crew.objects.get(id = crewId)
//         crew.present = False
//     }
//     if (present == 'unchecked'){
//         crew = Crew.objects.get(id = crewId)
//         crew.present = True
//     }
//     console.log (crew.name, crew.present)
// }

function updateAttendance(crewId, presence){
    console.log('User is logged in, sending data...')

        var url = 'update_Attendance/'
        console.log('URL:', url)
        console.log('crewId',crewId, 'presence',presence)


        fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'crewId':crewId, 'presence':presence})
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
            location.reload()
        })
}