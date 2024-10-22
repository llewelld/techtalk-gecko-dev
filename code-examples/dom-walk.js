function node_stats(global_ctx, local_ctx, node) {
    // Update the context
    local_ctx.depth += 1;
    local_ctx.breadth.push(node.childNodes.length);
    global_ctx.nodes += 1;
    global_ctx.maxdepth = Math.max(
        local_ctx.depth, global_ctx.maxdepth);

    // Recurse into child nodes
    for (child of node.childNodes) {
        child_ctx = structuredClone(local_ctx);
        child_ctx.breadth = local_ctx.breadth.
            slice(0, local_ctx.depth + 1);
        child_ctx = node_stats(global_ctx, child_ctx, child);

        // Recalculate the child breadths
        for (let i = local_ctx.depth + 1;
            i < child_ctx.breadth.length; ++i) {
            local_ctx.breadth[i] = (local_ctx.breadth[i]||0)
                + child_ctx.breadth[i];
        }
    }

    // Paint the DOM red
    if (node.style) {
        node.style.border = "1px dashed red";
    }

    // Move back up the tree
    local_ctx.depth -= 1;
    return local_ctx;
}

// Data available to all nodes
global_ctx = {
    "nodes": 0,
    "maxdepth": 0,
    "maxbreadth": 0
};

// Data that's local to the node and shared with the parent
local_ctx = {
    "depth": 0,
    "breadth": [1]
};

// Off we go
local_ctx = node_stats(global_ctx, local_ctx, document);
global_ctx.maxbreadth = Math.max.apply(null, local_ctx.breadth);

// Return the results (only strings allowed)
return JSON.stringify(global_ctx);
