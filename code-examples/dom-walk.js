function collect_node_stats(global_ctx, local_ctx, node) {
    // Update the context
    local_ctx.depth += 1;
    local_ctx.breadth.push(node.childNodes.length);
    global_ctx.nodes += 1;
    global_ctx.maxdepth = Math.max(
        local_ctx.depth, global_ctx.maxdepth);

    // Recurse into child nodes
    for (child of node.childNodes) {
        child_ctx = structuredClone(local_ctx);
        child_ctx.breadth = local_ctx.breadth.slice(
            0, local_ctx.depth + 1);
        child_ctx = collect_node_stats(
            global_ctx, child_ctx, child);

        // Recalculate the child breadths
        for (let i = local_ctx.depth + 1;
            i < child_ctx.breadth.length; ++i) {
            local_ctx.breadth[i] = (local_ctx.breadth[i]||0)
                + child_ctx.breadth[i];
        }
    }

    // Paint the DOM red
    if (node.style) {
        node.style.boxShadow = "inset 0px 0px 1px 0.5px red";
    }

    // Move back up the tree
    local_ctx.depth -= 1;
    return local_ctx;
}

function node_stats() {
    // Data available to all nodes
    let global_ctx = {
        "nodes": 0,
        "maxdepth": 0,
        "maxbreadth": 0
    }

    // Data local to the node and shared with the parent
    let local_ctx = {
        "depth": 0,
        "breadth": [1]
    }

    // Off we go
    local_ctx = collect_node_stats(
        global_ctx, local_ctx, document);
    global_ctx.maxbreadth = Math.max.apply(
        null, local_ctx.breadth);
    return global_ctx;
}

// Return the results (only strings allowed)
JSON.stringify(node_stats())
