# Plan

## Overview
- Algorithm / topic: Binary Search
- Audience: 初學者
- Primary teaching goal: 理解二元搜尋如何透過 `left`、`right`、`mid` 的更新，持續縮小有效區間
- Primary mode: pointer and control-flow explainer

## Core Structures
- Core data structure(s): 一個已排序主陣列 `main`
- Key state variables / pointers: `left`、`right`、`mid`
- Important boundaries or regions: 當前有效搜尋區間 `[left, right]`

## Key Teaching Points
- Key invariant(s): 只要目標值存在，它一定落在目前的 `[left, right]` 區間中
- Common confusion points:
  - 為什麼可以一次排除一半區間
  - `mid` 的角色到底是比較點還是答案位置
  - 為什麼更新 `left` 或 `right` 之後不會漏掉答案
- Local-to-global story: 每一次比較只排除一部分不可能的區間，但連續的區間縮減會快速收斂到答案位置

## Beat Outline
1. 建立已排序陣列與搜尋目標
2. 顯示初始 `left`、`right` 與第一個 `mid`
3. 比較目標值與 `mid` 的值
4. 排除不可能的一半區間
5. 更新 pointer 並縮小有效搜尋範圍
6. 重複直到找到答案

## Visual Priorities
- Stable semantic roles:
  - 預設元素：藍色
  - 當前 `mid`：黃色
  - 已排除區域：較淡或較暗
  - 找到的答案：綠色
  - `left` / `right` / `mid` pointer：各自有清楚標籤
- Required highlights:
  - 當前 `mid`
  - 當前有效搜尋區間
- Progress markers:
  - `left`、`right`、`mid` 的更新
  - 被排除區域逐步擴大
- Things to avoid:
  - 讓 pointer 同時過於搶眼
  - 沒有清楚表示哪一半被排除
  - 把比較與區間更新塞在同一拍造成閱讀壓力
