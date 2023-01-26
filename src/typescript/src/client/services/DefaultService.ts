/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_for_access_token_login_post } from '../models/Body_login_for_access_token_login_post';
import type { Data } from '../models/Data';
import type { SearchData } from '../models/SearchData';
import type { StoreData } from '../models/StoreData';
import type { StudentChatContinueData } from '../models/StudentChatContinueData';
import type { StudentChatStartData } from '../models/StudentChatStartData';
import type { SummariseData } from '../models/SummariseData';
import type { SummariseUrlData } from '../models/SummariseUrlData';
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
     * Student Chat Start
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static studentChatStartChatStudentStartPost(
        requestBody: StudentChatStartData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/chat/student/start',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Student Chat Continue
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static studentChatContinueChatStudentContinuePost(
        requestBody: StudentChatContinueData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/chat/student/continue',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Save Form
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static saveFormSaveFormPost(
        requestBody: StoreData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/save/form',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Run Alphacrucis Search
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static runAlphacrucisSearchSearchAlphacrucisPost(
        requestBody: SearchData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/search/alphacrucis',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Send User Signin Link
     * @param email
     * @returns any Successful Response
     * @throws ApiError
     */
    public static sendUserSigninLinkSendSigninLinkPost(
        email: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/send/signin-link',
            query: {
                'email': email,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Run Summarise With Query Raw
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static runSummariseWithQueryRawSummariseWithQueryRawPost(
        requestBody: SummariseData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/summarise/with-query/raw',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Run Summarise Url With Query
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static runSummariseUrlWithQuerySummariseWithQueryUrlPost(
        requestBody: SummariseUrlData,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/summarise/with-query/url',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Save Form
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static saveFormQueryFromTranscriptPost(
        requestBody: Data,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/query/from-transcript',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
