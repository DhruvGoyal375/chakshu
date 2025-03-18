import { AuditoryDescription } from '../audio/auditory_description.js';
import { Span } from '../audio/span.js';
declare abstract class FunctionsStore<S> {
    private prefix;
    private store;
    protected constructor(prefix: string, store: {
        [key: string]: S;
    });
    add(name: string, func: S): void;
    addStore(store: FunctionsStore<S>): void;
    lookup(name: string): S;
    private checkCustomFunctionSyntax_;
}
export type CustomQuery = (p1: Node) => Node[];
export declare class CustomQueries extends FunctionsStore<CustomQuery> {
    constructor();
}
export type CustomString = (p1: Node) => Span[];
export declare class CustomStrings extends FunctionsStore<CustomString> {
    constructor();
}
export type ContextFunction = (p1: Node[] | Node, p2: string | null) => () => string | AuditoryDescription[];
export declare class ContextFunctions extends FunctionsStore<ContextFunction> {
    constructor();
}
export type CustomGenerator = (store?: any, flag?: boolean) => string[] | void;
export declare class CustomGenerators extends FunctionsStore<CustomGenerator> {
    constructor();
}
export type SpeechRuleFunction = CustomQuery | CustomString | ContextFunction | CustomGenerator;
export {};
