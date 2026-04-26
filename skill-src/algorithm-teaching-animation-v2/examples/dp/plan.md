# Plan

## Overview
- Algorithm / topic: 0/1 Knapsack DP Table Construction
- Audience: 初學者
- Primary teaching goal: 理解 0/1 Knapsack 的每個 DP cell 如何在「不選當前物品」與「選當前物品」之間做選擇
- Primary mode: dynamic programming construction

## Core Structures
- Core data structure(s): 一個 DP 矩陣 `dp`
- Key state variables / pointers: 當前 `row`、`col`
- Important boundaries or regions: 已完成區域、當前 cell、依賴來源 cell

## Key Teaching Points
- Key invariant(s): 已填寫完成的 cell 都可作為後續狀態的合法依賴；每個新 cell 都來自合法依賴中的最佳選擇
- Common confusion points:
  - 每個 cell 到底代表什麼
  - 為什麼要依特定順序填表
  - 為什麼目前 cell 會依賴「不選」與「選」兩種候選來源
- Local-to-global story: 每次只計算一個 cell，但每個 cell 都在比較包含與不包含當前物品的最佳值，最終累積成完整最優解

## Beat Outline
1. 建立 DP 表格與 row / col 的意義
2. 聚焦第一個需要做選擇的 cell
3. 同時顯示「不選」與「選」兩個依賴來源
4. 將較佳結果寫入 cell
5. 擴大已完成區域並重複同樣規則
6. 收束成最終答案所在位置

## Visual Priorities
- Stable semantic roles:
  - 未處理 cell：藍色
  - 當前 cell：黃色
  - 已完成 cell：綠色
  - 依賴來源：橘色
- Required highlights:
  - 當前 cell
  - 依賴來源 cell
- Progress markers:
  - 已完成區域逐步擴大
  - 最終答案 cell 被明確標出
- Things to avoid:
  - 沒有說明 cell 的意義就直接填值
  - 同時高亮太多格子
  - 讓填表順序難以辨識
