"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[582],{9582:function(e,s,t){t.d(s,{Z:function(){return $}});var a=t(5893),n=t(7294),r=t(9008),i=t.n(r),o=t(1163),l=t(6426),c=t(8368),d=t(243),m=t(1799),u=t(8796),g=t(2525),x=t(2829),h=t(7886),f={src:"/_next/static/media/Logo.8ab847ad.gif",height:500,width:500},p=t(5675),b=t.n(p);function y(){let{chatData:e,setChatData:s}=(0,n.useContext)(h.p);function t(){s({...e,openModal:"chat"})}function r(){s({...e,openModal:"enquire"})}return(0,a.jsx)(c.p,{as:"nav",className:"bg-white shadow w-screen fixed z-10",children:e=>{let{open:s}=e;return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)("div",{className:"mx-auto px-4 sm:px-6 lg:px-8",children:(0,a.jsxs)("div",{className:"flex h-16 justify-between",children:[(0,a.jsxs)("div",{className:"flex",children:[(0,a.jsx)("div",{className:"-ml-2 mr-2 flex items-center md:hidden",children:(0,a.jsxs)(c.p.Button,{className:"inline-flex items-center justify-center p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-orange-500",children:[(0,a.jsx)("span",{className:"sr-only",children:"Open main menu"}),s?(0,a.jsx)(d,{className:"block h-6 w-6","aria-hidden":"true"}):(0,a.jsx)(m,{className:"block h-6 w-6","aria-hidden":"true"})]})}),(0,a.jsxs)("div",{className:"flex flex-shrink-0 items-center",children:[(0,a.jsx)(b(),{className:"block h-14 w-auto lg:hidden",src:f,alt:"Global Talent"}),(0,a.jsx)(b(),{className:"hidden h-12 w-auto lg:block",src:f,alt:"Global Talent"})]}),(0,a.jsxs)("div",{className:"hidden md:ml-6 md:flex md:space-x-8",children:[(0,a.jsx)("a",{href:"#MoreInfo",className:"inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-800 hover:text-orange-400 hover:border-orange-500",children:"More Info"}),(0,a.jsx)("a",{href:"#Reviews",className:"inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-800 hover:text-orange-400 hover:border-orange-500",children:"Reviews"}),(0,a.jsx)("a",{href:"#StudentExperience",className:"inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-800 hover:text-orange-400 hover:border-orange-500",children:"Student Experience"})]})]}),(0,a.jsxs)("div",{className:"flex items-center",children:[(0,a.jsxs)("button",{type:"button",onClick:t,className:"text-gray-800 flex-col text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",children:[(0,a.jsx)(u,{className:"h-5 w-5 text-orange-600","aria-hidden":"true"}),(0,a.jsx)("span",{className:"text-gray-800 text-xs",children:"Chat"})]}),(0,a.jsxs)("button",{type:"button",className:"text-gray-800 flex-col text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",onClick:()=>window.open("https://forms.gle/bJohSSgcd2g61WKSA"),children:[(0,a.jsx)(g,{className:"h-5 w-5 text-orange-600","aria-hidden":"true"}),(0,a.jsx)("span",{className:"text-gray-800 text-xs",children:"Apply"})]}),(0,a.jsxs)("button",{type:"button",onClick:r,className:"text-gray-800 flex-col text-md inline-flex items-center px-4 py-2 rounded-md shadow-sm hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",children:[(0,a.jsx)(x,{className:"h-5 w-5 text-orange-600","aria-hidden":"true"}),(0,a.jsx)("span",{className:"text-gray-800 text-xs",onClick:r,children:"Enquire"})]})]})]})}),(0,a.jsx)(c.p.Panel,{className:"md:hidden",children:(0,a.jsxs)("div",{className:"space-y-1 pt-2 pb-3",children:[(0,a.jsx)(c.p.Button,{as:"a",href:"#MoreInfo",className:"block border-l-4 border-orange-500 py-2 pl-3 pr-4 text-base font-medium text-orange-400 sm:pl-5 sm:pr-6",children:"More Info"}),(0,a.jsx)(c.p.Button,{as:"a",href:"#Reviews",className:"block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6",children:"Reviews"}),(0,a.jsx)(c.p.Button,{as:"a",href:"#StudentExperience",className:"block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6",children:"Student Experience"}),(0,a.jsx)(c.p.Button,{as:"a",href:"#blog",className:"block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-orange-300 sm:pl-5 sm:pr-6",children:"Blogs"})]})})]})}})}var j=t(1355),v=t(1909),N=t(9431),w=t(6245),k=t(6844);async function C(e,s){let t=e.originatorDetails.agent.firstName||"{agent_name}",a="";for(let s of e.messageHistory){let t=e.originatorDetails[s.originator].firstName,n=s.message;a+="".concat(t,": ").concat(n,"\n\n")}let n={agent_name:t,task_prompt:e.taskPrompt,transcript:a};e.googleIdToken&&(n.google_id_token=e.googleIdToken),e.assistanceToken&&(n.assistance_token=e.assistanceToken);let r=await (0,k.W)(n),i=[...e.messageHistory,{originator:"agent",message:r.agent_message,timestamp:Date.now()}],o={...e,messageHistory:i,assistanceToken:r.assistance_token};s(o)}let T=e=>{let s=e.messageHistory;if(0===s.length)return!1;let t=s[s.length-1];return"client"===t.originator},D=(e,s,t,a)=>{let n={...e.originatorDetails.client,[t]:a},r={...e.originatorDetails,client:n},i={...e,originatorDetails:r};return s(i),i};var S=function(e){let s=e.originator,{chatData:t}=(0,n.useContext)(h.p),r=t.originatorDetails[s].profilePictureUrl;if(null===r)return(0,a.jsx)(a.Fragment,{});let i=t.originatorDetails[s].firstName;return null===i?(0,a.jsx)("img",{className:"w-6 h-6 rounded-full -mt-3",src:r,alt:"Profile Picture"}):(0,a.jsx)("img",{className:"w-6 h-6 rounded-full -mt-3",src:r,alt:i})};let F=e=>new Date(e).toLocaleString();function P(){let{chatData:e}=(0,n.useContext)(h.p),s=null,t=()=>{null!=s&&s.scrollIntoView({behavior:"smooth"})};return(0,n.useEffect)(t,[e.messageHistory]),(0,n.useEffect)(()=>{t()},[e.messageHistory]),(0,a.jsxs)("div",{className:"flex-1 max-h-96 overflow-scroll",children:[(0,a.jsx)("div",{className:"flex flex-col h-full",children:e.messageHistory.map((s,t)=>{let{message:n,originator:r,timestamp:i}=s;F(i);let o=e.originatorDetails[r].firstName;return(0,a.jsx)("div",{className:"flex ".concat("client"===r?"justify-end":"justify-start"," mb-4"),children:(0,a.jsxs)("div",{className:"flex flex-col items-start p-2",children:[(0,a.jsx)("div",{className:"flex items-center",children:(0,a.jsx)("span",{className:"text-xs ml-2 leading-relaxed text-gray-400",children:o})}),(0,a.jsxs)("div",{className:"flex flex-col items-end",children:[(0,a.jsx)("div",{className:"py-2 px-4 rounded-xl rounded-br-none ".concat("client"===r?"bg-orange-400 text-white":"bg-gray-400 text-white"," max-w-xs"),children:n.replaceAll("{agent_name}",e.originatorDetails.agent.firstName?e.originatorDetails.agent.firstName:"agent").replaceAll("{client_name}",e.originatorDetails.client.firstName?e.originatorDetails.client.firstName:"client")}),(0,a.jsx)(S,{originator:r})]})]})},t)})}),(0,a.jsx)("div",{ref:e=>{s=e}})]})}function _(){let{chatData:e,setChatData:s}=(0,n.useContext)(h.p),[t,r]=(0,n.useState)(!0),i=async t=>{let a;let n=t.credential;if(console.log(n),void 0==n)return;let r=(0,w.Z)(n);console.log(r),e.originatorDetails.client.firstName=r.given_name,e.originatorDetails.client.lastName=r.family_name,e.originatorDetails.client.email=r.email,e.originatorDetails.client.profilePictureUrl=r.picture,e.googleIdToken=n,null===e.pendingQuestion?a=[{originator:"agent",message:"Hi {client_name}, it's great to meet you! Thank you for signing in. How can I help you today?",timestamp:Date.now()}]:(a=[{originator:"agent",message:"Hi {client_name}, it's great to meet you! Thank you for signing in.",timestamp:Date.now()},{originator:"client",message:e.pendingQuestion,timestamp:Date.now()}],e.pendingQuestion=null);let i=[...e.messageHistory,...a],o={...e,messageHistory:i};s(o),T(o)&&await C(o,s)};return((0,n.useEffect)(()=>{r(null==e.googleIdToken)},[e]),t)?(0,a.jsx)("div",{className:"max-w-xs m-auto pb-6",children:(0,a.jsx)(l.kZ,{onSuccess:i,onError:()=>{console.log("Login Failed")}})}):(0,a.jsx)(a.Fragment,{})}function H(){let{chatData:e,setChatData:s}=(0,n.useContext)(h.p),[t,r]=(0,n.useState)(""),i=t=>{let a={originator:"client",message:t,timestamp:Date.now()},n=[...e.messageHistory,a],r={...e,messageHistory:n};s(r),C(r,s)},o=e=>{r(e.target.value)},l=e=>{e.preventDefault(),i(t),r("")},c=e=>{e.preventDefault()};return(0,a.jsx)("div",{className:"flex items-center justify-between p-1 border-gray-200",children:(0,a.jsx)("form",{className:"flex w-full",onSubmit:c,children:(0,a.jsxs)("div",{className:"flex w-full bg-gray-400 items-center rounded-lg",children:[(0,a.jsx)("input",{type:"text",className:"w-full px-4 py-2 border border-gray-20000 rounded-l-md focus:outline-none focus:border-orange-600",placeholder:"Ask us about enrolment or application ...",value:t,onChange:o,disabled:T(e)}),(0,a.jsx)("button",{type:"submit",className:"bg-orange-400 w-12 justify-center h-full flex rounded-r-lg focus:ring-offset-2 hover:bg-gray-400 focus:ring-white",onClick:l,disabled:""===t||T(e),children:(0,a.jsx)(N,{className:"h-6 w-6 self-center text-white"})})]})})})}var I=function(){return(0,a.jsxs)("div",{className:"flex flex-col flex-1 h-96 bg-gray-800",children:[(0,a.jsx)(P,{}),(0,a.jsx)(_,{}),(0,a.jsx)(H,{})]})},M=function(){let{chatData:e,setChatData:s}=(0,n.useContext)(h.p),t=()=>{s({...e,openModal:null})};return(0,a.jsx)(j.u,{appear:!0,show:"chat"===e.openModal,as:n.Fragment,children:(0,a.jsxs)(v.V,{as:"div",className:"fixed inset-0 z-10 overflow-y-auto",onClose:t,children:[(0,a.jsx)(j.u.Child,{as:n.Fragment,enter:"ease-out duration-300",enterFrom:"opacity-0",enterTo:"opacity-100",leave:"ease-in duration-200",leaveFrom:"opacity-100",leaveTo:"opacity-0",children:(0,a.jsx)("div",{className:"fixed inset-0 bg-black bg-opacity-25"})}),(0,a.jsx)("div",{className:"fixed inset-0 overflow-y-auto",children:(0,a.jsx)("div",{className:"flex min-h-full items-center justify-center p-2 text-center",children:(0,a.jsx)(j.u.Child,{as:n.Fragment,enter:"ease-out duration-300",enterFrom:"opacity-0 scale-95",enterTo:"opacity-100 scale-100",leave:"ease-in duration-200",leaveFrom:"opacity-100 scale-100",leaveTo:"opacity-0 scale-95",children:(0,a.jsxs)(v.V.Panel,{className:"w-full rounded max-w-2xl transform bg-gray-800 overflow-visible mb-2 p-2 text-left align-middle shadow-5xl transition-all",children:[(0,a.jsx)("div",{className:"flex justify-end",children:(0,a.jsx)("button",{children:(0,a.jsx)(d,{className:"h-6 w-6 text-gray-500 rounded border border-gray-500 hover:bg-white focus:outline-none focus:ring-2 focus:ring-white focus:text-orange-200 sfocus:ring-offset-2","aria-hidden":"true",onClick:t})})}),(0,a.jsx)(I,{})]})})})})," "]})})},B=t(335);async function E(e){let s=e.originatorDetails.client;if(!s.agreeToTerms||!s.email||!s.phoneNumber||!s.firstName||!s.lastName||!s.enquiryMessage)return;let t={first_name:s.firstName,last_name:s.lastName,email:s.email,phone_number:s.phoneNumber,message:s.enquiryMessage,agree_to_terms:s.agreeToTerms};s.referrerTag&&(t.referrer_tag=s.referrerTag);let a=await (0,k.h)(t);return a}var q=t(5764),L=t(8505);function A(e){return(0,a.jsx)(a.Fragment,{children:(0,a.jsx)("div",{"aria-live":"assertive",className:"pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start z-50 sm:p-6",children:(0,a.jsx)("div",{className:"flex w-full flex-col items-center space-y-4 sm:items-end",children:(0,a.jsx)(j.u,{show:e.show,as:n.Fragment,enter:"transform ease-out duration-300 transition",enterFrom:"translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2",enterTo:"translate-y-0 opacity-100 sm:translate-x-0",leave:"transition ease-in duration-100",leaveFrom:"opacity-100",leaveTo:"opacity-0",children:(0,a.jsx)("div",{className:"pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5",children:(0,a.jsx)("div",{className:"p-4",children:(0,a.jsxs)("div",{className:"flex items-start",children:[(0,a.jsx)("div",{className:"flex-shrink-0",children:(0,a.jsx)(q,{className:"h-6 w-6 text-green-400","aria-hidden":"true"})}),(0,a.jsxs)("div",{className:"ml-3 w-0 flex-1 pt-0.5",children:[(0,a.jsx)("p",{className:"text-sm font-medium text-gray-900",children:"Successfully sent!"}),(0,a.jsx)("p",{className:"mt-1 text-sm text-gray-500",children:"We'll get back to you shortly"})]}),(0,a.jsx)("div",{className:"ml-4 flex flex-shrink-0",children:(0,a.jsxs)("button",{type:"button",className:"inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2",onClick:()=>{e.setShow(!1)},children:[(0,a.jsx)("span",{className:"sr-only",children:"Close"}),(0,a.jsx)(L,{className:"h-5 w-5","aria-hidden":"true"})]})})]})})})})})})})}var z=function(){let{chatData:e,setChatData:s}=(0,n.useContext)(h.p),[t,r]=(0,n.useState)(!1),[i,o]=(0,n.useState)(!1),[l,c]=(0,n.useState)(!1),d=(t,a)=>{D(e,s,a,t.target.value)};function m(){for(var e=arguments.length,s=Array(e),t=0;t<e;t++)s[t]=arguments[t];return s.filter(Boolean).join(" ")}(0,n.useEffect)(()=>{D(e,s,"agreeToTerms",t)},[t]),(0,n.useEffect)(()=>{o(u())},[e]);let u=()=>{let s=e.originatorDetails.client;return g(s.firstName)&&g(s.lastName)&&g(s.email)&&g(s.phoneNumber)&&g(s.enquiryMessage)&&!0===s.agreeToTerms},g=e=>null!=e&&""!==e,f=e=>{s({...e,openModal:null})},p=async t=>{t.preventDefault(),await E(e);let a=D(e,s,"enquiryMessage","");f(a),c(!0)};return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(j.u,{appear:!0,show:"enquire"===e.openModal,as:n.Fragment,children:(0,a.jsxs)(v.V,{as:"div",className:"relative z-10 ",onClose:()=>{f(e)},children:[(0,a.jsx)(j.u.Child,{as:n.Fragment,enter:"ease-out duration-300",enterFrom:"opacity-0",enterTo:"opacity-100",leave:"ease-in duration-200",leaveFrom:"opacity-100",leaveTo:"opacity-0",children:(0,a.jsx)("div",{className:"fixed inset-0 bg-black bg-opacity-25"})}),(0,a.jsx)("div",{className:"fixed inset-0 overflow-y-auto",children:(0,a.jsx)("div",{className:"flex min-h-full items-center justify-center p-4 text-center",children:(0,a.jsx)(j.u.Child,{as:n.Fragment,enter:"ease-out duration-300",enterFrom:"opacity-0 scale-95",enterTo:"opacity-100 scale-100",leave:"ease-in duration-200",leaveFrom:"opacity-100 scale-100",leaveTo:"opacity-0 scale-95",children:(0,a.jsxs)(v.V.Panel,{className:"w-full max-w-md transform overflow-hidden rounded-2xl bg-gray-800 p-6 text-left align-middle shadow-xl transition-all",children:[(0,a.jsxs)(v.V.Title,{as:"h3",className:"text-3xl font-medium inline-flex leading-none text-white space-x-1",children:[(0,a.jsx)(x,{className:"text-orange-400 w-8 animate-pulse"}),(0,a.jsx)("h1",{children:"Contact Us"})]}),(0,a.jsx)("div",{className:"mt-5",children:(0,a.jsxs)("form",{action:"#",method:"POST",className:"grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8",onSubmit:p,children:[(0,a.jsxs)("div",{children:[(0,a.jsx)("label",{htmlFor:"first-name",className:"block text-sm font-medium text-orange-400",children:"First name"}),(0,a.jsx)("div",{className:"mt-1",children:(0,a.jsx)("input",{type:"text",name:"first-name",id:"first-name",value:e.originatorDetails.client.firstName||"",onChange:e=>d(e,"firstName"),autoComplete:"given-name",className:"block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"})})]}),(0,a.jsxs)("div",{children:[(0,a.jsx)("label",{htmlFor:"last-name",className:"block text-sm font-medium text-orange-400",children:"Last name"}),(0,a.jsx)("div",{className:"mt-1",children:(0,a.jsx)("input",{type:"text",name:"last-name",id:"last-name",value:e.originatorDetails.client.lastName||"",onChange:e=>d(e,"lastName"),autoComplete:"family-name",className:"block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"})})]}),(0,a.jsxs)("div",{className:"sm:col-span-2",children:[(0,a.jsx)("label",{htmlFor:"email",className:"block text-sm font-medium text-orange-400",children:"Email"}),(0,a.jsx)("div",{className:"mt-1",children:(0,a.jsx)("input",{id:"email",name:"email",type:"email",value:e.originatorDetails.client.email||"",onChange:e=>d(e,"email"),autoComplete:"email",className:"block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"})})]}),(0,a.jsxs)("div",{className:"sm:col-span-2",children:[(0,a.jsx)("label",{htmlFor:"phone-number",className:"block text-sm font-medium text-orange-400",children:"Phone Number"}),(0,a.jsx)("div",{className:"relative mt-1 rounded-md shadow-sm",children:(0,a.jsx)("input",{type:"text",name:"phone-number",id:"phone-number",value:e.originatorDetails.client.phoneNumber||"",onChange:e=>d(e,"phoneNumber"),autoComplete:"tel",className:"block w-full rounded-md border-gray-300 py-3 px-4 focus:border-indigo-500 focus:ring-indigo-500",placeholder:"+61 1234 5678"})})]}),(0,a.jsxs)("div",{className:"sm:col-span-2",children:[(0,a.jsx)("label",{htmlFor:"message",className:"block text-sm font-medium text-orange-400",children:"Message"}),(0,a.jsx)("div",{className:"mt-1",children:(0,a.jsx)("textarea",{id:"message",name:"message",value:e.originatorDetails.client.enquiryMessage||"",onChange:e=>d(e,"enquiryMessage"),rows:4,className:"block w-full rounded-md border-gray-300 py-3 px-4 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"})})]}),(0,a.jsx)("div",{className:"sm:col-span-2",children:(0,a.jsxs)("div",{className:"flex items-start",children:[(0,a.jsx)("div",{className:"flex-shrink-0",children:(0,a.jsxs)(B.r,{checked:t,onChange:r,className:m(t?"bg-indigo-600":"bg-gray-200","relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"),children:[(0,a.jsx)("span",{className:"sr-only",children:"Agree to policies"}),(0,a.jsx)("span",{"aria-hidden":"true",className:m(t?"translate-x-5":"translate-x-0","inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out")})]})}),(0,a.jsx)("div",{className:"ml-3",children:(0,a.jsxs)("p",{className:"text-base text-gray-500",children:["By selecting this, you agree to the"," ",(0,a.jsx)("a",{href:"#",className:"font-medium text-orange-400 underline",children:"Privacy Policy"})," ","and"," ",(0,a.jsx)("a",{href:"#",className:"font-medium text-orange-400 underline",children:"Cookie Policy"}),"."]})})]})}),(0,a.jsx)("div",{className:"sm:col-span-2",children:(0,a.jsx)("button",{type:"submit",disabled:!i,className:m(i?" bg-indigo-600  hover:bg-indigo-700":" bg-gray-600","inline-flex w-full items-center justify-center rounded-md border border-transparent px-6 py-3 text-base font-medium text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"),children:"Let's talk"})})]})})]})})})})]})}),(0,a.jsx)(A,{show:l,setShow:c})]})},G=t(9762),Q=function(e){let{chatData:s,setChatData:t}=(0,n.useContext)(h.p),r=()=>{t({...s,openModal:"chat",pendingQuestion:e.question})};return(0,a.jsxs)("button",{className:e.buttonClassName,type:"button",onClick:r,children:[(0,a.jsx)(G,{className:e.bubbleClassName}),(0,a.jsx)("h3",{className:e.textClassName,children:e.question})]})},R=t(3614),U=t.n(R);function V(e){let s=(0,n.useRef)(),[t,r]=(0,n.useState)(),i=(0,n.useRef)(),[o,l]=(0,n.useState)();return[{ref:s,set:r,config:{strings:["Discover God's Purpose for you in <u>Ministry</u>","Discover God's Purpose for you in <u>Counselling </u>","Discover God's Purpose for you in <u>Education</u>","Discover God's Purpose for you in <u>Business</u>","Discover God's Purpose for your <u>Life</u>"],typeSpeed:5,backSpeed:25,backDelay:1200,loop:!0,loopCount:1,showCursor:!1,bindInputFocusEvents:!0}},{ref:i,set:l,config:{strings:["We will help you find the right course and connect you to your purpose","Don't wait and waste your talent","ASK US TODAY."],typeSpeed:15,backSpeed:10,backDelay:1350,startDelay:7e3,loop:!0,loopCount:1,showCursor:!1}}].map(e=>{(0,n.useEffect)(()=>{let s=new(U())(e.ref.current,e.config);return e.set(s),()=>{s.destroy()}},[])}),(0,a.jsxs)("div",{className:"w-screen h-screen",children:[(0,a.jsx)("img",{className:"absolute opacity-30 -z-10 w-screen h-screen md:hidden",src:e.portraitPicture,alt:e.alt}),(0,a.jsx)("img",{className:"absolute opacity-30 -z-10 w-screen h-screen hidden md:block",src:e.landscapePicture,alt:e.alt}),(0,a.jsxs)("div",{className:"grid grid-rows-6 w-screen h-screen",children:[(0,a.jsx)("div",{className:"row-span-1 lg:row-span-2"}),(0,a.jsxs)("div",{className:"space-y-6 w-screen",children:[(0,a.jsxs)("div",{className:"row-span-4 relative w-screen space-y-4 ",children:[(0,a.jsx)("hr",{className:"border-orange-400 border-2 w-10/12 ml-10"}),(0,a.jsx)("h1",{className:"text-5xl pl-10 tracking-normal leading-none",ref:s}),(0,a.jsx)("h3",{className:"text-xl pl-10 pr-10 tracking-wide leading-tight font-light text-gray-800 w-screen",ref:i})]}),(0,a.jsx)(Q,{question:e.chatButtonText,buttonClassName:"row-span-1 inset-10 relative bg-gray-800 inline-flex w-9/12 rounded-md py-1 px-4 shadow-sm hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 lg:w-1/3 lg:justify-self-end space-x-4",bubbleClassName:"-ml-1 self-center text-white h-12 w-12",textClassName:"text-sm font-medium text-white uppercase leading-none text-left place-self-center"})]}),(0,a.jsx)("div",{className:"w-screen"})]})]})}var W=t(1251);function Y(e){let{chatData:s,setChatData:t}=(0,n.useContext)(h.p);return(0,a.jsx)("div",{id:"MoreInfo",className:"relative h-max bg-white lg:h-screen",children:(0,a.jsxs)("div",{className:"mx-auto max-w-full lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8",children:[(0,a.jsx)("div",{className:"relative flex md:col-span-7 xl:inset-0",children:(0,a.jsx)("iframe",{className:"w-screen aspect-video mt-10 pl-2 pr-2 bg-orange-50 object-cover lg:p-6 lg:w-full",src:e.videoLink,title:e.videoTitle,allow:"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",allowFullScreen:!0})}),(0,a.jsx)("div",{className:"px-6 pt-10 pb-24 sm:pb-32 justify-self-center md:col-span-5 lg:px-0",children:(0,a.jsxs)("div",{className:"mx-auto flex flex-col space-y-6 max-w-2xl lg:mx-0",children:[(0,a.jsx)("hr",{className:"border-orange-400 border-2"}),(0,a.jsx)("h1",{className:"text-5xl capitalize tracking-normal leading-none",children:e.heading}),(0,a.jsx)("h3",{className:"text-xl w-4/5 tracking-wide leading-tight font-light text-orange-400",children:e.subHeading}),(0,a.jsx)(Q,{question:e.chatButtonText,buttonClassName:"bg-gray-800 px-4 py-2 text-sm text-left leading-none text-white shadow-sm hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 w-5/12",bubbleClassName:"-ml-1 mr-3 h-7 w-7",textClassName:"leading-none text-white text-sm text-left uppercase"}),(0,a.jsx)("div",{className:"h-11",children:(0,a.jsxs)("button",{type:"button",onClick:function(){t({...s,openModal:"enquire"})},className:" bg-gray-800 px-4 py-2 text-sm text-left leading-none text-white shadow-sm hover:bg-orange-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2",children:[(0,a.jsx)(W,{className:"-ml-1 mr-3 w-7 h-7 ","aria-hidden":"true"}),e.learnButtonText]})})]})})]})})}let K=()=>((0,n.useEffect)(()=>{},[]),null),O=(0,n.lazy)(()=>t.e(644).then(t.bind(t,1644))),Z=(0,n.lazy)(()=>t.e(70).then(t.bind(t,1070))),J=(0,n.lazy)(()=>t.e(794).then(t.bind(t,1794))),X=(0,n.lazy)(()=>t.e(56).then(t.bind(t,2056)));function $(e){let[s,t]=(0,n.useState)(h.W),r=(0,o.useRouter)(),c=r.query.tag,d=e=>{let{pathname:s,query:t}=r,a=new URLSearchParams(t);a.delete(e),r.replace({pathname:s,query:a.toString()},void 0,{shallow:!0})};return(0,n.useEffect)(()=>{null!=c&&(D(s,t,"referrerTag",c),d("tag"),console.log("tag:",c))},[c]),(0,n.useEffect)(()=>{let e=async()=>{if(null==s.googleIdToken||T(s)||!s.pendingQuestion)return;let e={originator:"client",message:s.pendingQuestion,timestamp:Date.now()},a=[...s.messageHistory,e],n={...s,messageHistory:a,pendingQuestion:null};t(n),await C(n,t)};e()},[s]),(0,a.jsxs)(a.Fragment,{children:[(0,a.jsxs)(i(),{children:[(0,a.jsx)("title",{children:"Global Talent"}),(0,a.jsx)("meta",{name:"viewport",content:"width=device-width, initial-scale=1"}),(0,a.jsx)("link",{rel:"icon",href:"/favicon.ico"}),(0,a.jsx)(K,{})]}),(0,a.jsx)(l.rg,{clientId:"332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com",children:(0,a.jsxs)(h.p.Provider,{value:{chatData:s,setChatData:t},children:[(0,a.jsx)(y,{}),(0,a.jsx)(M,{}),(0,a.jsx)(z,{}),(0,a.jsx)(V,{portraitPicture:e.data.hero.portraitPicture,landscapePicture:e.data.hero.landscapePicture,alt:e.data.hero.alt,chatButtonText:e.data.hero.chatButtonText},e.data.hero.id),(0,a.jsx)(Y,{heading:e.data.moreInfo.heading,subHeading:e.data.moreInfo.subHeading,learnButtonText:e.data.moreInfo.learnButtonText,learnButtonLink:e.data.moreInfo.learnButtonLink,chatButtonText:e.data.moreInfo.chatButtonText,videoLink:e.data.moreInfo.videoLink,videoTitle:e.data.moreInfo.videoTitle},e.data.moreInfo.id),(0,a.jsx)(n.Suspense,{fallback:(0,a.jsx)("div",{children:"Loading..."}),children:(0,a.jsx)(O,{careerSnapshot:e.data.reviews.careerSnapshot,careerSlogan:e.data.reviews.careerSlogan,sidePanels:e.data.reviews.sidePanels,featured:e.data.reviews.featured})}),(0,a.jsx)(n.Suspense,{fallback:(0,a.jsx)("div",{children:"Loading..."}),children:(0,a.jsx)(X,{})}),(0,a.jsx)(n.Suspense,{fallback:(0,a.jsx)("div",{children:"Loading..."}),children:(0,a.jsx)(Z,{id:e.data.blog.id,blogHeading:e.data.blog.blogsHeading,blogSubHeading:e.data.blog.blogsSubHeading,posts:e.data.blog.posts})}),(0,a.jsx)(n.Suspense,{fallback:(0,a.jsx)("div",{children:"Loading..."}),children:(0,a.jsx)(J,{})})]})}),";"]})}},7886:function(e,s,t){t.d(s,{W:function(){return n},p:function(){return r}});var a=t(7294);let n={openModal:null,googleIdToken:null,assistanceToken:null,taskPrompt:"You work for Global Talent. You are trying to sell Alphacrucis Courses. Your customer's name is {client_name}.  Assume that {client_name} is not able to access information from anywhere else except by talking to you. As such, do not redirect them to any website or other sources.\n\nKeep in mind the below points in everything you say:\n\n- Personalise with the customer's name\n- Clearly communicate course objectives, outcomes, and unique features\n- Ask open-ended questions to understand student's needs\n- Show genuine empathy and interest in student's situation\n- Provide data, testimonials, and case studies for credibility\n- Create a sense of urgency for enrolment\n- Ensure consistency in messaging, tone, and branding.",messageHistory:[{originator:"agent",message:"Hi, my name is {agent_name}. Before we begin, please sign in.",timestamp:Date.now()}],pendingQuestion:null,originatorDetails:{client:{},agent:{firstName:"Michael",profilePictureUrl:"https://www.w3schools.com/howto/img_avatar.png"}}},r=(0,a.createContext)({chatData:n,setChatData:e=>{}})}}]);