let startDate = document.getElementById('startDate')
// let endDate = document.getElementById('endDate')

startDate.addEventListener('change',(e)=>{
  let startDateVal = e.target.value
  document.getElementById('startDateSelected').innerText = startDateVal
})

// endDate.addEventListener('change',(e)=>{
//   let endDateVal = e.target.value
//   document.getElementById('endDateSelected').innerText = endDateVal
// })  

// code from https://www.codeply.com/p/zU0EWDmIfn
// commented out the code for end date.  our project only focuses on selecting single dates.