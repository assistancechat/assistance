import {
  component$,
  useStore,
  useContextProvider,
  Resource,
  useResource$,
  useClientEffect$
} from "@builder.io/qwik";
import { useLocation, DocumentHead } from "@builder.io/qwik-city";
import { getContent, RegisteredComponent, RenderContent, getBuilderSearchParams } from "@builder.io/sdk-qwik";

import sha224 from 'crypto-js/sha224';

import { HeroItem } from "~/components/widgets/Hero";
import { FeaturesItem } from "~/components/widgets/Features";
import { FaqsItem } from "~/components/widgets/Faqs";
import { CallToActionItem } from "~/components/widgets/CallToAction";
import { FormItem } from "~/components/widgets/Form";
import { GPTChatItem, ChatItem } from "~/components/widgets/Chat";

import { FormRecordIdContext, FormPromptIdContext, FormUpdateCounterContext, FormUpdateCounterState } from "~/providers/form";
import { GptContext, GptState } from "~/providers/gpt";

export const BUILDER_PUBLIC_API_KEY = '57b43c3a14484f6ebb27d8b26e9db047';
export const BUILDER_MODEL = "page";

// Input types can be found at:
// https://www.builder.io/c/docs/custom-components-input-types#required
export const CUSTOM_COMPONENTS: RegisteredComponent[] = [
  HeroItem,
  FeaturesItem,
  FaqsItem,
  CallToActionItem,
  FormItem,
  GPTChatItem,
  ChatItem,
];

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
      messages: []
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
      body: "{}",
      headers: {'Content-Type': 'application/json'} });

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

    const tokenResponse = await fetch('https://api.assistance.chat/token', {
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

  const location = useLocation();
  const builderContentRsrc = useResource$<any>(() => {
    return getContent({
      model: BUILDER_MODEL,
      apiKey: BUILDER_PUBLIC_API_KEY,
      options: getBuilderSearchParams(location.query),
      userAttributes: {
        urlPath: location.pathname || "/",
      },
    });
  });

  return (
    <Resource
      value={builderContentRsrc}
      onPending={() => <div>Loading...</div>}
      onResolved={(content) => (
        <RenderContent
          model={BUILDER_MODEL}
          content={content}
          apiKey={BUILDER_PUBLIC_API_KEY}
          customComponents={CUSTOM_COMPONENTS}
        />
      )}
    />
  );
});

export const head: DocumentHead = {
  title: "Career Assistance Chat",
  meta: [
    {
      name: "description",
      content:
        "",
    },
  ],
};
