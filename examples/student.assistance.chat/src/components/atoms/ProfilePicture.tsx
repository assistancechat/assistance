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

import { ChatContext, MessageOriginator } from "@/providers/chat";

function ProfilePicture(props: { originator: MessageOriginator }) {
  const originator = props.originator;

  const { chatData } = useContext(ChatContext);
  const profilePictureUrl =
    chatData.originatorDetails[originator].profilePictureUrl;

  if (profilePictureUrl === null) {
    return <></>;
  }

  const name = chatData.originatorDetails[originator].firstName;

  if (name === null) {
    return (
      <img
        className="w-6 h-6 rounded-full -mt-3"
        src={profilePictureUrl}
        alt="Profile Picture"
      />
    );
  }

  return (
    <img
      className="w-6 h-6 rounded-full -mt-3"
      src={profilePictureUrl}
      alt={name}
    />
  );
}

export default ProfilePicture;
