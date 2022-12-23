import {
  component$,
  useStore,
  useContextProvider,
  Resource,
  useResource$
} from "@builder.io/qwik";
import { useLocation, DocumentHead } from "@builder.io/qwik-city";
import { getContent, RegisteredComponent, RenderContent, getBuilderSearchParams } from "@builder.io/sdk-qwik";

import { HeroItem } from "~/components/widgets/Hero";
import { FeaturesItem } from "~/components/widgets/Features";
import { FaqsItem } from "~/components/widgets/Faqs";
import { CallToActionItem } from "~/components/widgets/CallToAction";
import { FormItem } from "~/components/widgets/Form";
import { GPTChatItem, ChatItem } from "~/components/widgets/Chat";

import { FormRecordIdContext, FormPromptIdContext } from "~/providers/form";
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
  const gptState = useStore<GptState>({
      accessToken: "",
      hashedAccessToken: "",
      agentName: "",
      promptTemplate: "",
      initialPrompt: "",
      messages: []
    },
    { recursive: true }
  );

  useContextProvider(FormRecordIdContext, formRecordIdState);
  useContextProvider(FormPromptIdContext, formPromptIdState);
  useContextProvider(GptContext, gptState);

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
