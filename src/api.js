import openSocket from 'socket.io-client'

const socket = openSocket('http://localhost:3001')
console.log("Connecting")

socket.on('connect', function () {
  console.log("I'm connected!")
})

socket.on('disconnect', function () {
  console.log("I'm disconnected!")
})


socket.on('data', data => {
  console.log("Got data", data)
})

window.socket = socket
