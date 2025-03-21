import { SemanticFont, SemanticType } from './semantic_meaning.js';
import { SemanticDefault } from './semantic_default.js';
import { SemanticNodeCollator } from './semantic_default.js';
import { SemanticNode } from './semantic_node.js';
export declare class SemanticNodeFactory {
    leafMap: SemanticNodeCollator;
    defaultMap: SemanticDefault;
    private idCounter_;
    makeNode(id: number): SemanticNode;
    makeUnprocessed(mml: Element): SemanticNode;
    makeEmptyNode(): SemanticNode;
    makeContentNode(content: string): SemanticNode;
    makeMultipleContentNodes(num: number, content: string): SemanticNode[];
    makeLeafNode(content: string, font: SemanticFont): SemanticNode;
    makeBranchNode(type: SemanticType, children: SemanticNode[], contentNodes: SemanticNode[], opt_content?: string): SemanticNode;
    private createNode_;
}
