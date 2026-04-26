# Plan

## Overview
- Algorithm / topic: Bubble Sort
- Audience: 初學者
- Primary teaching goal: 理解相鄰比較如何逐步把較大的值推向右側，並在每一輪結束後固定一個最終位置
- Primary mode: algorithm walkthrough

## Core Structures
- Core data structure(s): 一個主陣列 `main`
- Key state variables / pointers: `j`
- Important boundaries or regions: 本輪尚未固定的比較區間

## Key Teaching Points
- Key invariant(s): 每完成一輪，最右側的一個元素就會固定，不再參與後續比較
- Common confusion points:
  - 為什麼只比較相鄰元素也能完成排序
  - 為什麼較大的元素會逐步「冒泡」到右側
  - 為什麼每一輪都能固定一個位置
- Local-to-global story: 每次局部比較只修正一對元素的相對順序，但一連串相鄰交換會把較大的值逐步推到正確位置，最終完成全域排序

## Beat Outline
1. 建立初始陣列，說明排序目標
2. 將焦點放到目前比較的相鄰元素
3. 若順序錯誤，交換兩者並強調較大值往右移動
4. 繼續掃描同一輪剩餘位置
5. 在一輪結束時標記最右側固定位置
6. 重複多輪直到整個陣列排序完成

## Visual Priorities
- Stable semantic roles:
  - 預設元素：藍色
  - 目前比較中的元素：黃色
  - 本輪已固定元素：綠色
  - 指標 `j`：上方指標
- Required highlights:
  - 當前比較對
  - 每輪結束後固定的位置
- Progress markers:
  - `j` pointer 的移動
  - 已固定區域從右往左逐步擴大
- Things to avoid:
  - 同時 highlight 太多元素
  - 因局部操作重排整列陣列
  - 在畫面上塞入過多說明文字
