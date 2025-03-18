import { Span, SpanAttrs } from '../audio/span.js';
import * as srf from './speech_rule_functions.js';
export declare class SpeechRuleContext {
    customQueries: srf.CustomQueries;
    customStrings: srf.CustomStrings;
    contextFunctions: srf.ContextFunctions;
    customGenerators: srf.CustomGenerators;
    applyCustomQuery(node: Node, funcName: string): Node[];
    applySelector(node: Node, expr: string): Node[];
    applyQuery(node: Node, expr: string): Node;
    applyConstraint(node: Node, expr: string): boolean;
    constructString(node: Node, expr: string): string;
    constructSpan(node: Node, expr: string, def: SpanAttrs): Span[];
    private constructString_;
    parse(functions: [string, srf.SpeechRuleFunction][] | {
        [key: string]: srf.SpeechRuleFunction;
    }): void;
}
