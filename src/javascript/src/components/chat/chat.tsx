import { useRef } from '@builder.io/qwik';
interface ICBFunction {
  (event: any): void
}

interface Props {
  style: object,
  isTyping: boolean,
  show: boolean,
  user: {
    id: string,
    online: boolean,
    name: string,
    profile: string,
    connected: boolean
  },
  recepient: {
    id: string,
    profile: string
  },
  messages: {
    displayName: string,
    message: string,
    id: string,
    profile: string,
    timestamp: string
  }[],
  options?: {
    isAudioRecord?: boolean,
    isCamera?: boolean,
    isAttachment?: boolean,
    isSmiley?: boolean,
    inputDisabled?: boolean
  },
  onSend: ICBFunction,
  onHide: ICBFunction,
  onShow: ICBFunction
}

export const ChatX = ({
  isTyping = false,
  show = false,
  onHide,
  onShow,
  recepient,
  user,
  messages = [],
  options = {},
  onSend,
  style = {
    zIndex: '111',
    bottom: '0',
    fontSize: '12px',
    right: '24px',
    position: 'fixed',
    width: '360px',
    height: '500px',
    background: '#ffffff'
  }
}: Props) => {
  const { isAudioRecord, isCamera, isAttachment, isSmiley, inputDisabled } = options;
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const [message, setMessage] = useState("");

  useEffect(() => {
    scrollToBottom()
  }, [messages]);

  const handleSend = () => {
    onSend(message)
    setMessage("")
  }

  const handleChange = (value: string) => setMessage(value);

  return (
    <div className="chat-component">
      <div id="chat-window" style={style} className={`flex-1 justify-between flex flex-col h-screen shadow pb-3 mb-3 transition duration-500 transform ${show ? '' : 'translate-x-60 translate-y-96 scale-0'}`}>
        <div className="flex sm:items-center justify-between p-3 border-b-2 border-gray-200 bg-blue-500">
          {user.connected && <div className="flex items-center space-x-4">
            <img src={user.profile} alt="" className="w-5 sm:w-10 h-10 sm:h-10 rounded-full" />
            <div className="flex flex-col leading-tight">
              <div className="text-xl mt-1 flex items-center">
                <span className="text-white mr-3">{user.name}</span>
                <span className={`${user.online ? 'text-green-500' : 'text-grey-50'}`}>
                  <svg width="10" height="10">
                    <circle cx="5" cy="5" r="5" fill="currentColor"></circle>
                  </svg>
                </span>
              </div>
            </div>
          </div>}
          <div className="flex items-center space-x-2 float-right">
            <button onClick={() => { }} type="button" className="inline-flex items-center justify-center rounded-full h-6 w-6 transition duration-500 ease-in-out text-white hover:bg-gray-300 focus:outline-none">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd" />
              </svg>
            </button>
            <button onClick={(e) => onHide(e)} type="button" className="inline-flex items-center justify-center rounded-full h-6 w-6 transition duration-500 ease-in-out text-white hover:bg-gray-300 focus:outline-none">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        <div id="messages" className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch">
          {
            messages.map((data: any) => {
              let recepientUser = recepient.id !== data.from
              return (
                <div className="chat-message" key={data.id}>
                  <div className={`flex items-end ${recepientUser && 'justify-end'}`}>
                    <div className={`flex flex-col space-y-2 text-xs max-w-xs mx-2 ${recepientUser ? 'order-1 items-end' : 'order-2 items-start'}`}>
                      <div>
                        <span className={`px-4 py-2 rounded-lg inline-block ${recepientUser ? "rounded-br-none bg-blue-600 text-white" : "rounded-bl-none bg-gray-300 text-gray-600"}`}>
                          {data.message}
                        </span>
                      </div>
                    </div>
                    <img src={data.profile} alt="My profile" className={`w-6 h-6 rounded-full ${recepientUser ? "order-2" : "order-1"}`} />
                  </div>
                </div>
              )
            })
          }
          <div ref={messagesEndRef} />
        </div>
        <div className="border-t-2 border-gray-200 px-4 pt-4 mb-2 sm:mb-0">
          {
            isTyping && <svg className="-mt-10 absolute animate-bounce w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
            </svg>
          }
          <div className="relative flex">
            {
              isAudioRecord && (<span className="absolute inset-y-0 flex items-center">
                <button type="button" className="inline-flex items-center justify-center rounded-full h-12 w-12 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="h-6 w-6 text-gray-600">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path>
                  </svg>
                </button>
              </span>)
            }
            <input disabled={inputDisabled} value={message} onKeyDown={(e: any) => { if (e.key === 'Enter') handleSend() }} onChange={(e) => handleChange(e.target.value)} type="text" placeholder="Write Something" className="w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-12 bg-gray-200 rounded-full py-3" />
            <div className="absolute right-0 items-center inset-y-0 hidden sm:flex">
              {isAttachment && (<button type="button" className="inline-flex items-center justify-center rounded-full h-10 w-10 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="h-6 w-6 text-gray-600">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"></path>
                </svg>
              </button>)
              }
              {
                isCamera && (<button type="button" className="inline-flex items-center justify-center rounded-full h-10 w-10 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="h-6 w-6 text-gray-600">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                </button>)
              }
              {
                isSmiley && (<button type="button" className="inline-flex items-center justify-center rounded-full h-10 w-10 transition duration-500 ease-in-out text-gray-500 hover:bg-gray-300 focus:outline-none">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="h-6 w-6 text-gray-600">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </button>)
              }
              <button disabled={!user.connected} onClick={handleSend} type="button" className="inline-flex items-center justify-center rounded-full h-12 w-12 transition duration-500 ease-in-out text-white bg-blue-500 hover:bg-blue-400 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-6 w-6 transform rotate-90">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      <button onClick={(e) => onShow(e)} type="button" className={`z-10 chat-btn right-3 p-3 bottom-3 fixed inline-flex items-center justify-center rounded-full h-16 w-16 transition duration-500 ease-in-out text-white bg-blue-500 hover:bg-blue-400 focus:outline-none transform ${show ? 'scale-0' : ''}`}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
          <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
        </svg>
      </button>
    </div>
  )
}
