import {
  component$,
  useStore,
  useContextProvider,
  useClientEffect$
} from "@builder.io/qwik";
import { DocumentHead } from "@builder.io/qwik-city";

import sha224 from 'crypto-js/sha224';

import { FormRecordIdContext, FormPromptIdContext, FormUpdateCounterContext, FormUpdateCounterState } from "~/providers/FormContexts";
import { GptContext, GptState } from "~/providers/GptContext";


import Hero from "~/components/widgets/Hero";

import { SITE } from "~/config.mjs";

export default component$(() => {
  const formRecordIdState = useStore<Record<string, string>>({});
  const formPromptIdState = useStore<Record<string, string>>({});
  const formUpdateCounterState = useStore<FormUpdateCounterState>({
    counter: 0
  });
  const gptState = useStore<GptState>({
      accessToken: "",
      agentName: "",
      promptTemplate: "",
      initialPrompt: "",
      conversation: []
    },
    { recursive: true }
  );

  useContextProvider(FormRecordIdContext, formRecordIdState);
  useContextProvider(FormPromptIdContext, formPromptIdState);
  useContextProvider(FormUpdateCounterContext, formUpdateCounterState);
  useContextProvider(GptContext, gptState);

  useClientEffect$(async () => {
    const usernameResponse = await fetch("https://api.assistance.chat/temp-account", {
      method: 'POST',
      headers: {'Content-Type': 'application/json;charset=UTF-8'}
    });

    const usernameData = await usernameResponse.json()

    // This corresponds to a temporary anonymous account. The username is a
    // cryptographic token
    const username: string = usernameData["username"]

    // NOTE: This doesn't provide any extra security
    const password = sha224(username).toString()

    const details: Record<string, string> = {
        'username': username,
        'password': password,
        'grant_type': 'password'
    };

    const formBodyItems = [];
    for (const property in details) {
      const encodedKey = encodeURIComponent(property);
      const encodedValue = encodeURIComponent(details[property]);
      formBodyItems.push(encodedKey + "=" + encodedValue);
    }
    const formBody = formBodyItems.join("&");

    const tokenResponse = await fetch('https://api.assistance.chat/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formBody
    })

    const accessTokenData = await tokenResponse.json()

    gptState.accessToken = accessTokenData["access_token"]
    }, {
    eagerness: 'idle',
  });


  return (
    <>
      <Hero />
    </>
  );
});

export const head: DocumentHead = {
  title: SITE.title,
  meta: [
    {
      name: "description",
      content: SITE.description,
    },
  ],
};
