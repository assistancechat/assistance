import { useEffect, useState, lazy, Suspense } from "react";
import axios from "axios";
import sha224 from "crypto-js/sha224";

import Head from "next/head";
import { Inter } from "@next/font/google";

import { GoogleOAuthProvider } from "@react-oauth/google";

import Navbar from "@/components/NavBar";
import Hero from "@/components/Hero";
import MoreInfo from "@/components/MoreInfo";
import StudentExperience from "@/components/StudentExperience";
import Blog from "@/components/Blog";
import Footer from "@/components/Footer";

import { ChatContext, ChatContextData, DefaultChatData } from "@/contexts/chat";
import { ApiAccessContext } from "@/contexts/api-access";

const inter = Inter({ subsets: ["latin"] });

//create a lazy loaded component for the reviews
const Reviews = lazy(() => import("@/components/Reviews"));

export default function Home() {
  // Details on implementation https://stackoverflow.com/a/51573816/3912576
  const [chatData, setChatData] = useState<ChatContextData>(DefaultChatData);
  const value = { chatData, setChatData };

  const [apiAccessToken, setApiAccessToken] = useState<string | null>(null);

  // Get an API token for a freshly created anonymous account
  useEffect(() => {
    const fetchAndSetApiAccessToken = async () => {
      const usernameResponse = await fetch(
        "https://api.assistance.chat/temp-account",
        {
          method: "POST",
          headers: { "Content-Type": "application/json;charset=UTF-8" },
        }
      );

      const usernameData = await usernameResponse.json();

      // This corresponds to a temporary anonymous account. The username is a
      // cryptographic token
      const username: string = usernameData["username"];

      // NOTE: This doesn't provide any extra security
      const password = sha224(username).toString();

      const details: Record<string, string> = {
        username: username,
        password: password,
        grant_type: "password",
      };

      const formBodyItems = [];
      for (const property in details) {
        const encodedKey = encodeURIComponent(property);
        const encodedValue = encodeURIComponent(details[property]);
        formBodyItems.push(encodedKey + "=" + encodedValue);
      }
      const formBody = formBodyItems.join("&");

      const tokenResponse = await fetch("https://api.assistance.chat/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
        body: formBody,
      });

      const accessTokenData = await tokenResponse.json();

      setApiAccessToken(accessTokenData["access_token"]);

      console.log(
        `User logged in with token: ${accessTokenData["access_token"]}`
      );
    };

    fetchAndSetApiAccessToken().catch((err) => console.error(err));
  }, []);

  return (
    <>
      <Head>
        <title>Global Talent</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <GoogleOAuthProvider clientId="332533892028-gmefpu618mrv51k25lhpjtfn09mep8kq.apps.googleusercontent.com">
        <ApiAccessContext.Provider value={apiAccessToken}>
          <ChatContext.Provider value={value}>
            <Navbar />
            <Hero />
            <MoreInfo />
            <Suspense fallback={<div>Loading...</div>}>
              <Reviews />
            </Suspense>
            <StudentExperience />
            <Blog />
            <Footer />
          </ChatContext.Provider>
        </ApiAccessContext.Provider>
      </GoogleOAuthProvider>
      ;
    </>
  );
}
