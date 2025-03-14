//
// Copyright 2015-21 Volker Sorge
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @file Utility class for caching levels during tree walking.
 * @author volker.sorge@gmail.com (Volker Sorge)
 */

export class Levels<T> {
  /**
   * Array caching levels.
   */
  private level_: T[][] = [];

  /**
   * Pushes a new level onto the stack.
   *
   * @param level The new level.
   */
  public push(level: T[]) {
    this.level_.push(level);
  }

  /**
   * Pops a level off the stack.
   *
   * @returns The old top level.
   */
  public pop(): T[] {
    return this.level_.pop();
  }

  /**
   * Peeks at the top level off the stack without popping it.
   *
   * @returns The top level.
   */
  public peek(): T[] {
    return this.level_[this.level_.length - 1] || null;
  }

  /**
   * Retrieves the index of an element on the top most level of the stack.
   *
   * @param element The element to look up.
   * @returns The index, -1 if element is not contained.
   */
  public indexOf(element: T): number | null {
    const last = this.peek();
    return !last ? null : last.indexOf(element);
  }

  /**
   * Checks for an element that satisfies the given predicate on the top most
   * level of the stack.  In ES6 this should be simply an array.find!
   *
   * @param pred A predicate for testing.
   * @returns The element matching the predicate.
   */
  public find(pred: (p1: T) => boolean): T | null {
    const last = this.peek();
    if (!last) {
      return null;
    }
    for (let i = 0, l = last.length; i < l; i++) {
      if (pred(last[i])) {
        return last[i];
      }
    }
    return null;
  }

  /**
   * Retrieves an element at specified index from the top level of the stack if
   * it exists.
   *
   * @param index The index of the element to retrieves.
   * @returns The element at the position.
   */
  public get(index: number): T | null {
    const last = this.peek();
    return !last || index < 0 || index >= last.length ? null : last[index];
  }

  /**
   * @returns The current depth of the levels.
   */
  public depth(): number {
    return this.level_.length;
  }

  /**
   * @returns The clone of this object.
   */
  public clone(): Levels<T> {
    const levels = new Levels<T>();
    levels.level_ = this.level_.slice(0);
    return levels;
  }

  /**
   * @override
   */
  public toString() {
    let str = '';
    for (let i = 0, level; (level = this.level_[i]); i++) {
      str +=
        '\n' +
        level.map(function (x) {
          return x.toString();
        });
    }
    return str;
  }
}
