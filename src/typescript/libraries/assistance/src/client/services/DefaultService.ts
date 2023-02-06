/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChatData } from '../models/ChatData';
import type { ChatResponse } from '../models/ChatResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Chat
     * @param requestBody
     * @returns ChatResponse Successful Response
     * @throws ApiError
     */
    public static chatChatPost(
        requestBody: ChatData,
    ): CancelablePromise<ChatResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: 'https://api.assistance.chat/chat',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
