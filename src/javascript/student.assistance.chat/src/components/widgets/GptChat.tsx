import {
  component$,
  useContext,
  useTask$,
} from '@builder.io/qwik';
import { FormRecordIdContext, FormPromptIdContext, FormUpdateCounterContext } from "~/providers/FormContexts";
import { GptContext } from "~/providers/GptContext";

import Chat from "~/components/widgets/Chat";

export const GPTChat = component$((props: {agentName: string, prompt: string}) => {
  const formRecordIdState = useContext(FormRecordIdContext);
  const formPromptIdState = useContext(FormPromptIdContext);
  const formUpdateCounterState = useContext(FormUpdateCounterContext);
  const gptState = useContext(GptContext);

  useTask$(() => {
    gptState.promptTemplate = props.prompt
    gptState.agentName = props.agentName
  })

  useTask$(({track}) => {
    const template = track(() => gptState.promptTemplate);
    const clientName = track(() => formRecordIdState['preferredName']);
    const agentName = track(() => gptState.agentName);
    track(() => formUpdateCounterState.counter);

    gptState.initialPrompt = template
      .replaceAll("{clientName}", clientName)
      .replaceAll("{agentName}", agentName)
      .replaceAll("{formContents}", JSON.stringify(formPromptIdState, null, 2))
  })

  const preferredName = formRecordIdState['preferredName']
  const email = formRecordIdState['email']

  if (preferredName == null || preferredName == "" || email == null || email == "") {
    return <></>
  }

  return (
    <div>
      <Chat
        disabled={false}
        conversation={gptState.conversation}
        // conversation={[{message:'Test'}, {message:'Test'}]}
        fieldsToWaitFor={[]}>
      </Chat>
      <div id="gpt-assistance-chat"></div>
    </div>
  );
})
