# Plan

## Overview
- Algorithm / topic: Breadth-First Search (BFS)
- Audience: 初學者
- Primary teaching goal: 理解 BFS 如何透過 queue 與 visited 狀態，一層一層向外探索 graph
- Primary mode: graph traversal explainer

## Core Structures
- Core data structure(s): 一個 graph、visited 狀態表、一個 queue 概念
- Key state variables / pointers: `current`
- Important boundaries or regions: 當前 frontier 與已訪問節點集合

## Key Teaching Points
- Key invariant(s): 所有已加入 visited 的節點都不會再被重複探索；queue 中的節點代表接下來要按層處理的 frontier
- Common confusion points:
  - BFS 與 DFS 的差異在哪裡
  - 為什麼 BFS 會一層一層展開
  - 為什麼 visited 要及早標記
- Local-to-global story: 每次只處理 queue front 的一個節點，但依序將其鄰居加入 queue，最終形成按層擴張的探索順序

## Beat Outline
1. 建立 graph 與起點
2. 標記起點為已訪問，作為第一層 frontier
3. 聚焦當前節點並展開其鄰居
4. 將尚未訪問的鄰居標記為下一層 frontier
5. 重複直到 queue 為空
6. 收束成完整遍歷順序

## Visual Priorities
- Stable semantic roles:
  - 未訪問節點：藍色
  - 當前節點：黃色
  - 已訪問節點：綠色
  - frontier / queue 候選：橘色
- Required highlights:
  - 當前節點
  - 本輪新加入 frontier 的節點
- Progress markers:
  - 已訪問節點逐步擴大
  - 當前探索焦點移動
- Things to avoid:
  - graph 位置頻繁改變
  - 一次標出太多角色卻沒有主焦點
  - 只看到節點變色，卻看不出 traversal story
