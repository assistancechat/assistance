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

import { useContext } from "react";
import { ChatBubbleOvalLeftEllipsisIcon } from "@heroicons/react/24/outline";

import { ChatContext } from "@/providers/chat";

function StartChatWithQuestionButton(props: {
  question: string;
  buttonClassName: string;
  bubbleClassName: string;
  textClassName: string;
}) {
  const { chatData, setChatData } = useContext(ChatContext);

  const startChatWithQuestion = () => {
    setChatData({
      ...chatData,
      openModel: true,
      pendingQuestion: props.question,
    });
  };

  return (
    <button
      className={props.buttonClassName}
      type="button"
      onClick={startChatWithQuestion}
    >
      <ChatBubbleOvalLeftEllipsisIcon className={props.bubbleClassName} />
      <h3 className={props.textClassName}>{props.question}</h3>
    </button>
  );
}

export default StartChatWithQuestionButton;
