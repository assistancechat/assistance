import { component$, useContext } from "@builder.io/qwik";
import { GptContext } from "~/providers/GptContext";

import Chat from "~/components/Chat";

export default component$(() => {
  const gptState = useContext(GptContext);

  return (
    <div>
      <Chat
        disabled={false}
        conversation={gptState.conversation}
        fieldsToWaitFor={[{ recordId: "name" }]}
      ></Chat>
      <div id="gpt-assistance-chat"></div>
    </div>
  );
});
