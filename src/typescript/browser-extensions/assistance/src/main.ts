import brain from "./img/brain.svg";

declare global {
  interface Window {
    _gmailjs: Gmail;
    gmail: Gmail;
  }
}

const loaderId = setInterval(() => {
  if (!window._gmailjs) {
    return;
  }

  clearInterval(loaderId);
  startExtension(window._gmailjs);
}, 100);

function startExtension(gmail: Gmail) {
  console.log("Extension loading...");
  window.gmail = gmail;

  gmail.observe.on("load", () => {
    const userEmail = gmail.get.user_email();
    console.log("Hello, " + userEmail + ". This is your extension talking!");

    addBrainButton(gmail);

    gmail.observe.on("view_email", (domEmail) => {
      console.log("Looking at email:", domEmail);
      const emailData = gmail.new.get.email_data(domEmail);
      console.log("Email data:", emailData);
    });

    gmail.observe.on("compose", (compose) => {
      console.log("New compose window is opened!", compose);
    });
  });
}

const addBrainButton = (gmail: Gmail) => {
  const googleBanner = document.querySelector(".gb_ve.gb_te");

  const button = document.createElement("div");
  button.classList.add("brain-button");

  const anchor = document.createElement("a");
  anchor.classList.add("brain-button-link");
  anchor.role = "button";

  const brainWrapper = document.createElement("img");
  brainWrapper.src = brain;
  brainWrapper.width = 24;

  anchor.appendChild(brainWrapper);
  button.appendChild(anchor);

  googleBanner?.prepend(button);

  button.onclick = () => {
    const overview = getOverviews(gmail);
    let innerHtml = "<form>";
    overview.fromAddresses.forEach((address) => {
      innerHtml += `<input type="checkbox" id="${address}" name="${address}" value="${address}">`;
      innerHtml += `<label for="${address}">${address}</label><br>`;
    });
    innerHtml += "</form>";

    // innerHtml += "<h3>Subjects:</h3><ul>";
    // overview.subject.forEach((subject) => {
    //   innerHtml += `<li>${subject}</li>`;
    // });
    // innerHtml += "</ul>";

    gmail.tools.add_modal_window("Email Assistance Chat", innerHtml, () => {
      getOverviews(gmail);
      gmail.tools.remove_modal_window();
    });
  };
};

const getOverviews = (gmail: Gmail) => {
  // @ts-ignore
  const threads = gmail.cache.threadCache as Record<string, GmailNewThreadData>;
  const overview = {
    fromAddresses: new Set<string>(),
    subject: new Set<string>(),
  };

  Object.entries(threads).forEach(([threadId, threadData]) => {
    threadData.emails.forEach((email) => {
      overview.fromAddresses.add(email.from.address);
      overview.subject.add(email.subject);
    });
  });

  return overview;
};

export {};
