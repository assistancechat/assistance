"use strict";

const GmailFactory = require("gmail-js");
const jQuery = require("jquery");

window._gmailjs = window._gmailjs || new GmailFactory.Gmail(jQuery);
