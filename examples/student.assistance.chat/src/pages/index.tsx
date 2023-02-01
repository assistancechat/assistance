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

import { useState, lazy, Suspense } from "react";

import Head from "next/head";
import { Inter } from "@next/font/google";

import { GoogleOAuthProvider } from "@react-oauth/google";

import Navbar from "@/components/NavBar";
import ChatModal from "@/components/ChatModal";
import Hero from "@/components/Hero";
import MoreInfo from "@/components/MoreInfo";
import StudentExperience from "@/components/StudentExperience";
import Blog from "@/components/Blog";
import Footer from "@/components/Footer";

import {
  ChatContext,
  ChatContextData,
  DefaultChatData,
} from "@/providers/chat";

const inter = Inter({ subsets: ["latin"] });

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import("@/components/Reviews"));

export default function Home() {
  // Details on implementation https://stackoverflow.com/a/51573816/3912576
  const [chatData, setChatData] = useState<ChatContextData>(DefaultChatData);
  const value = { chatData, setChatData };

  return (
    <>
      <Head>
        <title>Global Talent</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <GoogleOAuthProvider clientId="332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com">
        <ChatContext.Provider value={value}>
          <Navbar />
          <ChatModal />
          <Hero />
          <MoreInfo />
          <Suspense fallback={<div>Loading...</div>}>
            <Reviews />
          </Suspense>
          <StudentExperience />
          <Blog />
          <Footer />
        </ChatContext.Provider>
      </GoogleOAuthProvider>
      ;
    </>
  );
}