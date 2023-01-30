/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_for_access_token_login_post } from '../models/Body_login_for_access_token_login_post';
import type { StudentChatData } from '../models/StudentChatData';
import type { Token } from '../models/Token';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Login For Access Token
     * @param formData
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static loginForAccessTokenLoginPost(
        formData: Body_login_for_access_token_login_post,
    ): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Temp Account
     * @returns any Successful Response
     * @throws ApiError
     */
    public static tempAccountTempAccountPost(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/temp-account',
        });
    }

    /**
     * Student Chat
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static studentChatChatStudentPost(
        requestBody: StudentChatData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/chat/student',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
