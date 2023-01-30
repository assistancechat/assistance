import { React, useState, useEffect } from 'react'
import { Transition } from '@headlessui/react'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { ellipsis } from '../images/ellipsis.svg'

const chatData = [
  {
    id: 1,
    name: 'George Paul Thompson',
    profilepictureurl: 'https://www.w3schools.com/howto/img_avatar.png',
    text: 'Hi, how are you?',
    timestamp: '2021-03-01 12:02:00'
  },
  {
    id: 2,
    name: 'user',
    profilepictureurl: 'https://www.w3schools.com/howto/img_avatar2.png',
    text: 'I am fine, thanks. How are you?',
    timestamp: '2021-03-01 12:03:00'
  },
  {
    id: 3,
    name: 'George Paul Thompson',
    profilepictureurl: 'https://www.w3schools.com/howto/img_avatar.png',
    text: 'I am fine, thanks. How are you?',
    timestamp: '2021-03-01 12:04:00'
  },
  {
    id: 4,
    name: 'user',
    profilepictureurl: 'https://www.w3schools.com/howto/img_avatar2.png',
    text: 'I am fine, thanks. How are you?',
    timestamp: '2021-03-01 12:05:00'
  }
]

//create a timestamp function
const timeStampFunction = () => {
  const date = new Date()
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()
  return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}
  

//chat history component
function ChatHistory() {
  const [chatHistory, setChatHistory] = useState(chatData)
  const [isTyping, setIsTyping] = useState(false)

  // function to add a new message to the chat history
  const addNewMessage = (newMessage) => {
    setChatHistory([...chatHistory, newMessage])
  }

  //if the chat history sends a "...?..." message, the user is typing, set istyping state to true, display the ellipsis.svg as the most recent message in the chat history
  useEffect(() => {
    if (chatHistory[chatHistory.length - 1].message === '...?...') {
      setIsTyping(true)
    } else {
      setIsTyping(false)
    }
  }, [chatHistory])

  //if that chat history sends a "...!..." message, the user is not typing, set istyping state to false, remove the ellipsis.svg from the chat history
  useEffect(() => {
    if (chatHistory[chatHistory.length - 1].message === '...!...') {
      setIsTyping(false)
    }
  }, [chatHistory])

  //set the istyping state to false once new message is received that is not "...?..." or "...!..."
  useEffect(() => {
    if (
      chatHistory[chatHistory.length - 1].message !== '...?...' &&
      chatHistory[chatHistory.length - 1].message !== '...!...'
    ) {
      setIsTyping(false)
    }
  }, [chatHistory])


  // function to render the chat history
  const renderChatHistory = () => {
    return chatHistory.map((chat) => {
      return (
        <div
          key={chat.id}
          className={`flex ${
            chat.name === 'user' ? 'justify-end' : 'justify-start'
          } mb-4`}
        >
          <div className='flex flex-col items-end'>
            <div className='flex items-center'>
              <span className='text-xs text-gray-400 mr-2'>
                {chat.timestamp}
              </span>
              <span className='text-xs text-gray-400'>{chat.name}</span>
            </div>
            <div className='flex flex-col items-end'>
              <div
                className={`py-2 px-4 rounded-xl rounded-br-none ${
                  chat.name === 'user'
                    ? 'bg-orange-300 text-white'
                    : 'bg-gray-800 text-white'
                } max-w-xs`}
              >
                {chat.text}
              </div>
              <img
                className='w-6 h-6 rounded-full -mt-3'
                src={chat.profilepictureurl}
                alt={chat.name}
              />
            </div>
          </div>
        </div>
      )
    })

  }

  return (
    <div className='flex-1 h-full overflow-y-auto'>
      <div className='flex flex-col-reverse h-full'>
        {renderChatHistory()}
        <Transition
          show={isTyping}
          enter='transition ease-out duration-100'
          enterFrom='transform opacity-0 scale-95'
          enterTo='transform opacity-100 scale-100'
          leave='transition ease-in duration-75'
          leaveFrom='transform opacity-100 scale-100'
          leaveTo='transform opacity-0 scale-95'
        >
          <div className='flex justify-end mb-4'>
            <div className='flex flex-col items-end'>
              <div className='flex items-center'>
                <span className='text-xs text-gray-400 mr-2'>...</span>
                <span className='text-xs text-gray-400'>user</span>
              </div>
              <div className='flex flex-col items-end'>
                <div className='py-2 px-4 rounded-xl rounded-br-none bg-blue-600 text-white max-w-xs'>
                  <img src={ellipsis} className='w-4 h-4' alt='ellipsis' />
                </div>
                <img
                  className='w-6 h-6 rounded-full -mt-3'
                  src='https://www.w3schools.com/howto/img_avatar2.png'
                  alt='user'
                />
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  )
}

// chat input component
function ChatInput({ addNewMessage }) {
  const [message, setMessage] = useState('')

  // function to handle the message input
  const handleMessageInput = (e) => {
    setMessage(e.target.value)
  }

  // function to handle the message submit
  const handleMessageSubmit = (e) => {
    e.preventDefault()
    if (message !== '') {
      addNewMessage({
        id: 5,
        name: 'user',
        profilepictureurl: 'https://www.w3schools.com/howto/img_avatar2.png',
        message: message,
        timestamp: timeStampFunction,
      })
      setMessage('')
    }
  }

  // function that prevents the user from submitting the form if it is empty
  const handleFormSubmit = (e) => {
    e.preventDefault()
  }

  // function that passes a message to the chat history component if the user is typing
  const handleTyping = () => {
    addNewMessage({
      id: 5,
      name: 'user',
      profilepictureurl: 'https://www.w3schools.com/howto/img_avatar2.png',
      message: '...?...',
      timestamp: timeStampFunction,
    })
  }

  // function that passages a message to the chat history component if the user stops typing after 3 seconds
  const handleTypingTimeout = () => {
    addNewMessage({
      id: 4,
      name: 'user',
      profilepictureurl: 'https://www.w3schools.com/howto/img_avatar2.png',
      message: '...!...',
      timestamp: '2021-03-01 12:05:00'
    })
  }

  return (
    <div className='flex items-center justify-between p-4 border-t border-gray-200'>
      <form className='flex w-full' onSubmit={handleFormSubmit}>
        <div className='flex w-full items-center'>
          <input
            type='text'
            className='w-full px-4 py-2 border border-gray-200 rounded-full focus:outline-none focus:border-blue-500'
            placeholder='Type a message...'
            value={message}
            onChange={handleMessageInput}
            onKeyDown={ handleTyping}
          />
          <button type='submit' className='ml-4'>
            <PaperAirplaneIcon className='w-6 h-6 text-blue-500' />
          </button>
        </div>
      </form>
    </div>
  )
}

// chat component
function Chat() {
  const [chatHistory, setChatHistory] = useState()

  // function to add a new message to the chat history
  const addNewMessage = (newMessage) => {
    setChatHistory([newMessage, ...chatHistory])
  }

  return (
    <div className='flex flex-col flex-1 h-full'>
      <ChatHistory chatHistory={chatHistory} />
      <ChatInput addNewMessage={addNewMessage} />
    </div>
  )
}

export default Chat
