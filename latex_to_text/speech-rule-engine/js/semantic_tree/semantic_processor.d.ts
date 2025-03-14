import { SemanticFont } from './semantic_meaning.js';
import { SemanticNode } from './semantic_node.js';
import { SemanticNodeFactory } from './semantic_node_factory.js';
export declare class SemanticProcessor {
    private static readonly FENCE_TO_PUNCT_;
    private static readonly MML_TO_LIMIT_;
    private static readonly MML_TO_BOUNDS_;
    private static readonly CLASSIFY_FUNCTION_;
    private static readonly MATHJAX_FONTS;
    private static instance;
    funcAppls: {
        [key: string]: SemanticNode;
    };
    private factory_;
    static getInstance(): SemanticProcessor;
    static tableToMultiline(table: SemanticNode): SemanticNode;
    static number(node: SemanticNode): void;
    static classifyMultiline(multiline: SemanticNode): void;
    static classifyTable(table: SemanticNode): SemanticNode;
    private static detectCaleyTable;
    private static cayleySpacing;
    static proof(node: Element, semantics: string, parse: (p1: Element[]) => SemanticNode[]): SemanticNode;
    static findSemantics(node: Element, attr: string, opt_value?: string): boolean;
    static getSemantics(node: Element): {
        [key: string]: string;
    };
    static removePrefix(name: string): string;
    static separateSemantics(attr: string): {
        [key: string]: string;
    };
    private static matchSpaces_;
    private static getSpacer_;
    private static fenceToPunct_;
    private static classifyFunction_;
    private static propagateFunctionRole_;
    private static getFunctionOp_;
    private static tableToMatrixOrVector_;
    private static tableToVector_;
    private static binomialForm_;
    private static tableToMatrix_;
    private static tableToSquare_;
    private static getComponentRoles_;
    private static tableToCases_;
    private static rewriteFencedLine_;
    private static rowToLine_;
    private static assignRoleToRow_;
    private static nextSeparatorFunction_;
    private static meaningFromContent;
    private static numberRole_;
    private static exprFont_;
    static compSemantics(node: SemanticNode, field: string, sem: any): void;
    private static purgeFences_;
    private static rewriteFencedNode_;
    private static rewriteFence_;
    private static propagateFencePointer_;
    private static classifyByColumns_;
    private static isEndRelation_;
    private static isPureRelation_;
    private static computeColumns_;
    private static testColumns_;
    setNodeFactory(factory: SemanticNodeFactory): void;
    getNodeFactory(): SemanticNodeFactory;
    identifierNode(leaf: SemanticNode, font: SemanticFont, unit: string): SemanticNode;
    implicitNode(nodes: SemanticNode[]): SemanticNode;
    text(leaf: SemanticNode, type: string): SemanticNode;
    row(nodes: SemanticNode[]): SemanticNode;
    limitNode(mmlTag: string, children: SemanticNode[]): SemanticNode;
    tablesInRow(nodes: SemanticNode[]): SemanticNode[];
    mfenced(open: string | null, close: string | null, sepValue: string | null, children: SemanticNode[]): SemanticNode;
    fractionLikeNode(denom: SemanticNode, enume: SemanticNode, linethickness: string, bevelled: boolean): SemanticNode;
    tensor(base: SemanticNode, lsub: SemanticNode[], lsup: SemanticNode[], rsub: SemanticNode[], rsup: SemanticNode[]): SemanticNode;
    pseudoTensor(base: SemanticNode, sub: SemanticNode[], sup: SemanticNode[]): SemanticNode;
    font(font: string): SemanticFont;
    proof(node: Element, semantics: {
        [key: string]: string;
    }, parse: (p1: Element[]) => SemanticNode[]): SemanticNode;
    inference(node: Element, semantics: {
        [key: string]: string;
    }, parse: (p1: Element[]) => SemanticNode[]): SemanticNode;
    getLabel(_node: Element, children: Element[], parse: (p1: Element[]) => SemanticNode[], side: string): SemanticNode;
    getFormulas(node: Element, children: Element[], parse: (p1: Element[]) => SemanticNode[]): {
        conclusion: SemanticNode;
        premises: SemanticNode;
    };
    findNestedRow(nodes: Element[], semantic: string, opt_value?: string): Element;
    cleanInference(nodes: NodeList): Element[];
    operatorNode(node: SemanticNode): SemanticNode;
    private constructor();
    private implicitNode_;
    private infixNode_;
    private explicitMixed_;
    private concatNode_;
    private prefixNode_;
    private splitRoles;
    private splitOps;
    private splitSingles;
    private postfixNode_;
    private combineUnits_;
    private getMixedNumbers_;
    private getTextInRow_;
    private relationsInRow_;
    private operationsInRow_;
    private wrapPostfix;
    private wrapFactor;
    private addFactor;
    private operationsTree_;
    private appendOperand_;
    private appendDivisionOp_;
    private appendLastOperand_;
    private appendMultiplicativeOp_;
    private appendAdditiveOp_;
    private appendExistingOperator_;
    private getFencesInRow_;
    private fences_;
    private neutralFences_;
    private combineFencedContent_;
    private horizontalFencedNode_;
    private classifyHorizontalFence_;
    private setExtension_;
    private getPunctuationInRow_;
    private punctuatedNode_;
    private dummyNode_;
    private accentRole_;
    private accentNode_;
    private makeLimitNode_;
    private getFunctionsInRow_;
    private getFunctionArgs_;
    private getIntegralArgs_;
    private functionNode_;
    private bigOpNode_;
    private integralNode_;
    private functionalNode_;
    private fractionNode_;
    private scriptNode_;
    private findNestedRow_;
}
