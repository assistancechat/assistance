// Copyright (C) 2023 Assistance.Chat contributors

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { useState, lazy, Suspense, useEffect } from 'react'

import Head from 'next/head'
import { Inter } from '@next/font/google'

import { GoogleOAuthProvider } from '@react-oauth/google'

import Navbar from '@/components/NavBar'
import ChatModal from '@/components/ChatModal'
import HeroOpening from '@/components/HeroOpening'
import MoreInfo from '@/components/MoreInfo'

//data
import * as data from '@/components/data/general.json'

import {
  ChatContext,
  ChatContextData,
  DefaultChatData,
  MessageHistoryItem
} from '@/providers/chat'

import { mostRecentChatIsClient } from '@/utilities/flow'
import { callChatApi } from '@/utilities/call-api'
import { NoFallbackError } from 'next/dist/server/base-server'

const inter = Inter({ subsets: ['latin'] })

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import('@/components/Reviews'))
const Blog = lazy(() => import('@/components/Blog'))
const Footer = lazy(() => import('@/components/Footer'))

export default function Home() {
  // Details on implementation https://stackoverflow.com/a/51573816/3912576
  const [chatData, setChatData] = useState<ChatContextData>(DefaultChatData)
  const value = { chatData, setChatData }

  useEffect(() => {
    const appendPendingQuestionIfReady = async () => {
      if (chatData.googleIdToken == null) {
        return
      }

      if (mostRecentChatIsClient(chatData)) {
        return
      }

      if (!chatData.pendingQuestion) {
        return
      }

      const messageHistoryToAppend: MessageHistoryItem = {
        originator: 'client',
        message: chatData.pendingQuestion,
        timestamp: Date.now()
      }

      const updatedMessageHistory = [
        ...chatData.messageHistory,
        messageHistoryToAppend
      ]

      const updatedChatData = {
        ...chatData,
        messageHistory: updatedMessageHistory,
        pendingQuestion: null
      }

      setChatData(updatedChatData)
      await callChatApi(updatedChatData, setChatData)
    }

    appendPendingQuestionIfReady()
  }, [chatData])

  return (
    <>
      <Head>
        <title>Global Talent</title>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <GoogleOAuthProvider clientId='332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com'>
        <ChatContext.Provider value={value}>
          <Navbar />
          <ChatModal />
          <HeroOpening 
            key={data.hero.id}
            portraitPicture={data.hero.portraitPicture}
            landscapePicture={data.hero.landscapePicture}
            alt={data.hero.alt}
            courseTitle={data.hero.courseTitle}
            headLine1={data.hero.headLine1}
            headLine2={data.hero.headLine2}
            headLine3={data.hero.headLine3}
            headLine4={data.hero.headLine4}
            headLine5={data.hero.headLine5}
            headLine6={data.hero.headLine6}
            subHeading={data.hero.subHeading}
            learnButtonText={data.hero.learnButtonText}
            learnButtonLink={data.hero.learnButtonLink}
            ChatButtonText={data.hero.ChatButtonText}
          />
          <MoreInfo
            key={data.moreInfo.id}
            heading={data.moreInfo.heading}
            subHeading={data.moreInfo.subHeading}
            learnButtonText={data.moreInfo.learnButtonText}
            learnButtonLink={data.moreInfo.learnButtonLink}
            ChatButtonText={data.moreInfo.ChatButtonText}
            videoLink={data.moreInfo.videoLink}
            videoTitle={data.moreInfo.videoTitle}
          />
          <Suspense fallback={<div>Loading...</div>}>
            <Reviews
              key={data.reviews.id}
              careerSnapshot={data.reviews.careerSnapshot}
              careerSlogan={data.reviews.careerSlogan}
              sidePanel={data.reviews.sidePanel}
              featured={data.reviews.featured}
            />
          </Suspense>
          <Suspense fallback={<div>Loading...</div>}>
            <Blog
              key={data.blog.id}
              blogsHeading={data.blog.blogsHeading}
              blogsSubHeading={data.blog.blogsSubHeading}
              posts={data.blog.posts}
            />
          </Suspense>
          <Suspense fallback={<div>Loading...</div>}>
            <Footer />
          </Suspense>
        </ChatContext.Provider>
      </GoogleOAuthProvider>
      ;
    </>
  )
}
