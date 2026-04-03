"use client";

import { Thread } from "@/components/assistant-ui/thread";
import { PriceSnapshotTool } from "@/components/tools/price-snapshot/PriceSnapshotTool";
import { PurchaseStockTool } from "@/components/tools/purchase-stock/PurchaseStockTool";
import { ThreadList } from "@/components/assistant-ui/thread-list";
import { useAui, AuiProvider, Suggestions } from "@assistant-ui/react";

function ThreadWithSuggestions() {
  const aui = useAui({
    suggestions: Suggestions([
      {
        title: "有哪些关于恐怖活动的法律？",
        label: "有哪些关于恐怖活动的法律？",
        prompt: "有哪些关于恐怖活动的法律？",
      },
      {
        title: "请具体说说第二十条法律",
        label: "请具体说说第二十条法律",
        prompt: "请具体说说第二十条法律",
      },
    ]),
  });
  return (
    <AuiProvider value={aui}>
      <Thread />
    </AuiProvider>
  );
}

export default function Home() {
  return (
    <div className="flex h-dvh">
      <div className="max-w-md">
        <ThreadList />
      </div>
      <div className="flex-grow">
        <ThreadWithSuggestions />
        <PriceSnapshotTool />
        <PurchaseStockTool />
      </div>
    </div>
  );
}
