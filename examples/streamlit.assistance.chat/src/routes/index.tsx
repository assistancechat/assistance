import { component$, useStore, useContextProvider } from "@builder.io/qwik";
import { DocumentHead } from "@builder.io/qwik-city";

import {
  FormRecordIdContext,
  FormPromptIdContext,
  FormUpdateCounterContext,
  FormUpdateCounterState,
} from "~/providers/FormContexts";
import { GptContext, GptState } from "~/providers/GptContext";

import App from "~/components/App";

import { SITE } from "~/config.mjs";

export default component$(() => {
  const formRecordIdState = useStore<Record<string, string>>({});
  const formPromptIdState = useStore<Record<string, string>>({});
  const formUpdateCounterState = useStore<FormUpdateCounterState>({
    counter: 0,
  });
  const gptState = useStore<GptState>(
    {
      accessToken: "",
      agentName: "",
      promptTemplate: "",
      initialPrompt: "",
      conversation: [],
    },
    { recursive: true }
  );

  useContextProvider(FormRecordIdContext, formRecordIdState);
  useContextProvider(FormPromptIdContext, formPromptIdState);
  useContextProvider(FormUpdateCounterContext, formUpdateCounterState);
  useContextProvider(GptContext, gptState);

  return (
    <>
      <App />
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
