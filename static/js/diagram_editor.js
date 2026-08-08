(function () {
    'use strict';

    const SVG_NS = 'http://www.w3.org/2000/svg';
    const VIEWPORT_WIDTH = 960;
    const VIEWPORT_HEIGHT = 540;
    const WORLD_WIDTH = 8000;
    const WORLD_HEIGHT = 5200;
    const MIN_NODE_WIDTH = 80;
    const MIN_NODE_HEIGHT = 44;
    const MAX_NODE_WIDTH = 2400;
    const MAX_NODE_HEIGHT = 1800;
    const MIN_FONT_SIZE = 10;
    const MAX_FONT_SIZE = 52;
    const MAX_EDGE_BEND = 1200;
    const MAX_NODES = 80;
    const MAX_EDGES = 200;
    const MAX_FREE_ARROWS = 100;
    const MAX_GROUPS = 32;
    const MAX_REGIONS = 40;
    const MIN_ZOOM = 0.1;
    const MAX_ZOOM = 4;
    const ARROW_REGION_SNAP_PX = 32;
    const DIAGRAM_MARKER_REGEX = /\[\[diyagram:([A-Za-z0-9_-]{1,64000})\]\]/g;
    const editorModal = document.getElementById('diagramEditorModal');
    const viewerModal = document.getElementById('diagramViewerModal');

    if (!editorModal || !viewerModal) return;

    const canvas = document.getElementById('diagramEditorCanvas');
    const viewportLayer = document.getElementById('diagramEditorViewport');
    const groupsLayer = document.getElementById('diagramEditorGroups');
    const edgesLayer = document.getElementById('diagramEditorEdges');
    const nodesLayer = document.getElementById('diagramEditorNodes');
    const regionsLayer = document.getElementById('diagramEditorRegions');
    const regionDefs = document.getElementById('diagramEditorRegionDefs');
    const handlesLayer = document.getElementById('diagramEditorHandles');
    const miniMap = document.getElementById('diagramMiniMap');
    const miniMapContent = document.getElementById('diagramMiniMapContent');
    const miniMapViewport = document.getElementById('diagramMiniMapViewport');
    const connectButton = document.getElementById('diagramConnectBtn');
    const freeArrowButton = document.getElementById('diagramFreeArrowBtn');
    const duplicateButton = document.getElementById('diagramDuplicateBtn');
    const arrangeButton = document.getElementById('diagramArrangeBtn');
    const snapButton = document.getElementById('diagramSnapBtn');
    const undoButton = document.getElementById('diagramUndoBtn');
    const redoButton = document.getElementById('diagramRedoBtn');
    const deleteButton = document.getElementById('diagramDeleteBtn');
    const copyButton = document.getElementById('diagramCopyBtn');
    const pasteButton = document.getElementById('diagramPasteBtn');
    const alignHorizontalButton = document.getElementById('diagramAlignHorizontalBtn');
    const alignVerticalButton = document.getElementById('diagramAlignVerticalBtn');
    const distributeButton = document.getElementById('diagramDistributeBtn');
    const groupButton = document.getElementById('diagramGroupBtn');
    const ungroupButton = document.getElementById('diagramUngroupBtn');
    const inspectorToggleButton = document.getElementById('diagramInspectorToggleBtn');
    const editorLayout = editorModal.querySelector('.diagram-editor-layout');
    const zoomOutButton = document.getElementById('diagramZoomOutBtn');
    const zoomInButton = document.getElementById('diagramZoomInBtn');
    const fitButton = document.getElementById('diagramFitBtn');
    const zoomValue = document.getElementById('diagramZoomValue');
    const versionsButton = document.getElementById('diagramVersionsBtn');
    const versionsPanel = document.getElementById('diagramVersionsPanel');
    const versionsCloseButton = document.getElementById('diagramVersionsCloseBtn');
    const saveVersionButton = document.getElementById('diagramSaveVersionBtn');
    const versionList = document.getElementById('diagramVersionList');
    const insertButton = document.getElementById('insertDiagramBtn');
    const titleInput = document.getElementById('diagramTitleInput');
    const labelInput = document.getElementById('diagramNodeLabelInput');
    const shapeSelect = document.getElementById('diagramNodeShapeSelect');
    const nodeWidthInput = document.getElementById('diagramNodeWidthInput');
    const nodeHeightInput = document.getElementById('diagramNodeHeightInput');
    const nodeWidthValue = document.getElementById('diagramNodeWidthValue');
    const nodeHeightValue = document.getElementById('diagramNodeHeightValue');
    const nodeFontSizeInput = document.getElementById('diagramNodeFontSizeInput');
    const nodeFontSizeValue = document.getElementById('diagramNodeFontSizeValue');
    const nodeLinkInput = document.getElementById('diagramNodeLinkInput');
    const nodeLinkOpenButton = document.getElementById('diagramNodeLinkOpenBtn');
    const nodeInspector = document.getElementById('diagramNodeInspector');
    const edgeInspector = document.getElementById('diagramEdgeInspector');
    const edgeInspectorTitle = document.getElementById('diagramEdgeInspectorTitle');
    const edgeInspectorBadge = document.getElementById('diagramEdgeInspectorBadge');
    const inspectorEmpty = document.getElementById('diagramInspectorEmpty');
    const edgeLabelInput = document.getElementById('diagramEdgeLabelInput');
    const edgeDescriptionInput = document.getElementById('diagramEdgeDescriptionInput');
    const edgeStyleSelect = document.getElementById('diagramEdgeStyleSelect');
    const edgeRouteSelect = document.getElementById('diagramEdgeRouteSelect');
    const edgeBendInput = document.getElementById('diagramEdgeBendInput');
    const edgeBendValue = document.getElementById('diagramEdgeBendValue');
    const arrowAnchors = document.getElementById('diagramArrowAnchors');
    const arrowStartAnchor = document.getElementById('diagramArrowStartAnchor');
    const arrowEndAnchor = document.getElementById('diagramArrowEndAnchor');
    const multiInspector = document.getElementById('diagramMultiInspector');
    const multiSelectionCount = document.getElementById('diagramMultiSelectionCount');
    const groupNameField = document.getElementById('diagramGroupNameField');
    const groupLabelInput = document.getElementById('diagramGroupLabelInput');
    const regionMenuButton = document.getElementById('diagramRegionMenuBtn');
    const regionInspector = document.getElementById('diagramRegionInspector');
    const regionManager = document.getElementById('diagramRegionManager');
    const regionList = document.getElementById('diagramRegionList');
    const regionCount = document.getElementById('diagramRegionCount');
    const regionLabelInput = document.getElementById('diagramRegionLabelInput');
    const regionOperationSelect = document.getElementById('diagramRegionOperationSelect');
    const regionToneSelect = document.getElementById('diagramRegionToneSelect');
    const regionSymbol = document.getElementById('diagramRegionSymbol');
    const regionMemberList = document.getElementById('diagramRegionMemberList');
    const regionMemberCount = document.getElementById('diagramRegionMemberCount');
    const regionMemberApplyButton = document.getElementById('diagramRegionMemberApplyBtn');
    const differenceBaseField = document.getElementById('diagramDifferenceBaseField');
    const differenceBaseSelect = document.getElementById('diagramDifferenceBaseSelect');
    const toneButtons = Array.from(document.querySelectorAll('[data-diagram-tone]'));
    const selectionBadge = document.getElementById('diagramSelectionBadge');
    const status = document.getElementById('diagramCanvasStatus');
    const nodeCount = document.getElementById('diagramNodeCount');
    const edgeCount = document.getElementById('diagramEdgeCount');
    const viewerStage = document.getElementById('diagramViewerStage');
    const viewerTitle = document.getElementById('diagramViewerTitle');
    const editorTitle = document.getElementById('diagramEditorTitle');
    const editDiagramButton = document.getElementById('editDiagramBtn');
    const downloadDiagramButton = document.getElementById('downloadDiagramBtn');
    const downloadDiagramPngButton = document.getElementById('downloadDiagramPngBtn');
    const downloadDiagramPdfButton = document.getElementById('downloadDiagramPdfBtn');
    const viewerInfo = document.getElementById('diagramViewerInfo');
    const viewerInfoTitle = document.getElementById('diagramViewerInfoTitle');
    const viewerInfoText = document.getElementById('diagramViewerInfoText');
    const viewerInfoClose = document.getElementById('diagramViewerInfoClose');

    let activeTextarea = null;
    let graph = createCycleTemplate();
    let selected = null;
    let selectedNodeIds = new Set();
    let connectMode = false;
    let connectSource = null;
    let dragState = null;
    let labelDragState = null;
    let regionLabelDragState = null;
    let regionMemberDraft = null;
    let history = [];
    let redoHistory = [];
    let nextNodeNumber = 10;
    let snapEnabled = true;
    let editingMarker = null;
    let viewerContext = null;
    let clipboardGraph = null;
    let spacePanActive = false;
    let panState = null;
    let pinchState = null;
    const activeTouchPointers = new Map();
    let edgeHandleState = null;
    let freeArrowEndpointState = null;
    let freeArrowDropAnchor = '';
    let nodeResizeState = null;
    let viewState = { zoom: 1, panX: 0, panY: 0 };

    function svgElement(name, attributes) {
        const element = document.createElementNS(SVG_NS, name);
        Object.entries(attributes || {}).forEach(([key, value]) => {
            element.setAttribute(key, String(value));
        });
        return element;
    }

    function initializeTooltips(root) {
        if (!window.bootstrap || !bootstrap.Tooltip || !root) return;
        root.querySelectorAll('.diagram-tool-btn[title]').forEach((element) => {
            if (!element.disabled || element.parentElement.classList.contains('diagram-tooltip-proxy')) return;
            const proxy = document.createElement('span');
            proxy.className = 'diagram-tooltip-proxy';
            proxy.tabIndex = 0;
            proxy.title = element.title;
            element.removeAttribute('title');
            element.before(proxy);
            proxy.appendChild(element);
        });
        root.querySelectorAll('[title]').forEach((element) => {
            bootstrap.Tooltip.getOrCreateInstance(element, {
                container: 'body',
                placement: 'bottom',
                trigger: 'hover focus',
                delay: { show: 320, hide: 80 }
            });
        });
    }

    function createUid() {
        if (window.crypto && typeof window.crypto.randomUUID === 'function') {
            return `d${window.crypto.randomUUID().replace(/-/g, '').slice(0, 20)}`;
        }
        return `d${Date.now().toString(36)}${Math.random().toString(36).slice(2, 10)}`;
    }

    function syncNextNodeNumber(value = graph) {
        const numericIds = (value && Array.isArray(value.nodes) ? value.nodes : [])
            .map((node) => /^n(\d+)$/.exec(String(node.id || '')))
            .filter(Boolean)
            .map((match) => Number(match[1]));
        nextNodeNumber = Math.max(9, ...numericIds, 0) + 1;
    }

    function takeNextNodeId() {
        const usedIds = new Set(graph.nodes.map((node) => node.id));
        while (usedIds.has(`n${nextNodeNumber}`)) nextNodeNumber += 1;
        const id = `n${nextNodeNumber}`;
        nextNodeNumber += 1;
        return id;
    }

    function createBlankTemplate() {
        return { version: 5, uid: createUid(), title: 'Yeni diyagram', nodes: [], edges: [], arrows: [], groups: [], regions: [] };
    }

    function createFlowTemplate() {
        return {
            version: 5,
            uid: createUid(),
            title: 'Basit akış',
            nodes: [
                { id: 'n1', label: 'Başlangıç', shape: 'terminal', tone: 'green', x: 150, y: 270 },
                { id: 'n2', label: 'Karar', shape: 'decision', tone: 'gold', x: 460, y: 270 },
                { id: 'n3', label: 'Birinci sonuç', shape: 'process', tone: 'blue', x: 770, y: 155 },
                { id: 'n4', label: 'İkinci sonuç', shape: 'process', tone: 'neutral', x: 770, y: 385 }
            ],
            edges: [
                { from: 'n1', to: 'n2', label: '', style: 'solid' },
                { from: 'n2', to: 'n3', label: 'Evet', style: 'solid' },
                { from: 'n2', to: 'n4', label: 'Hayır', style: 'dashed' }
            ],
            arrows: [],
            groups: [],
            regions: []
        };
    }

    function createCycleTemplate() {
        return {
            version: 5,
            uid: createUid(),
            title: 'Basit döngü',
            nodes: [
                { id: 'n1', label: 'Başlangıç', shape: 'terminal', tone: 'green', x: 150, y: 270 },
                { id: 'n2', label: 'Uygula', shape: 'process', tone: 'blue', x: 430, y: 150 },
                { id: 'n3', label: 'Kontrol et', shape: 'decision', tone: 'gold', x: 730, y: 270 },
                { id: 'n4', label: 'Yeniden düzenle', shape: 'process', tone: 'neutral', x: 430, y: 405 }
            ],
            edges: [
                { from: 'n1', to: 'n2', label: '', style: 'solid' },
                { from: 'n2', to: 'n3', label: '', style: 'solid' },
                { from: 'n3', to: 'n4', label: 'Hayır', style: 'solid' },
                { from: 'n4', to: 'n2', label: 'Tekrar', style: 'dashed' }
            ],
            arrows: [],
            groups: [],
            regions: []
        };
    }

    function createSpiralTemplate() {
        const center = { x: 480, y: 270 };
        const nodes = [
            { id: 'n1', label: 'Başla', shape: 'terminal', tone: 'green', x: 480, y: 270, width: 78, height: 46, fontSize: 13 },
            { id: 'n2', label: 'Hedef koy', shape: 'process', tone: 'blue', x: 575, y: 270, width: 94, height: 46, fontSize: 13 },
            { id: 'n3', label: 'Dene', shape: 'process', tone: 'gold', x: 550, y: 198, width: 86, height: 46, fontSize: 13 },
            { id: 'n4', label: 'Gözlemle', shape: 'process', tone: 'green', x: 430, y: 170, width: 98, height: 46, fontSize: 13 },
            { id: 'n5', label: 'Değerlendir', shape: 'decision', tone: 'gold', x: 325, y: 270, width: 108, height: 76, fontSize: 13 },
            { id: 'n6', label: 'Yenile', shape: 'process', tone: 'neutral', x: 390, y: 385, width: 92, height: 46, fontSize: 13 },
            { id: 'n7', label: 'Derinleştir', shape: 'process', tone: 'blue', x: 550, y: 410, width: 108, height: 46, fontSize: 13 },
            { id: 'n8', label: 'Genişlet', shape: 'process', tone: 'gold', x: 690, y: 270, width: 96, height: 46, fontSize: 13 },
            { id: 'n9', label: 'Yeni bağlam', shape: 'process', tone: 'green', x: 600, y: 120, width: 106, height: 46, fontSize: 13 },
            { id: 'n10', label: 'Uygula', shape: 'process', tone: 'blue', x: 360, y: 95, width: 92, height: 46, fontSize: 13 },
            { id: 'n11', label: 'Ölç', shape: 'process', tone: 'gold', x: 200, y: 270, width: 82, height: 46, fontSize: 13 },
            { id: 'n12', label: 'Uyumla', shape: 'process', tone: 'neutral', x: 325, y: 470, width: 94, height: 46, fontSize: 13 },
            { id: 'n13', label: 'Olgunlaştır', shape: 'process', tone: 'blue', x: 635, y: 480, width: 108, height: 46, fontSize: 13 },
            { id: 'n14', label: 'Yeni düzey', shape: 'terminal', tone: 'green', x: 815, y: 270, width: 106, height: 48, fontSize: 13 }
        ];
        const edges = nodes.slice(0, -1).map((node, index) => {
            const next = nodes[index + 1];
            const dx = next.x - node.x;
            const dy = next.y - node.y;
            const length = Math.max(Math.hypot(dx, dy), 1);
            const normal = { x: -dy / length, y: dx / length };
            const midpoint = { x: (node.x + next.x) / 2, y: (node.y + next.y) / 2 };
            const outward = { x: midpoint.x - center.x, y: midpoint.y - center.y };
            const direction = (normal.x * outward.x) + (normal.y * outward.y) >= 0 ? 1 : -1;
            return {
                from: node.id,
                to: next.id,
                label: index === 3 ? '1. tur' : index === 6 ? '2. tur' : '',
                style: 'solid',
                route: 'curve',
                bend: direction * Math.min(46, 18 + (index * 2.2))
            };
        });
        return {
            version: 5,
            uid: createUid(),
            title: 'Spiral ilerleme',
            nodes,
            edges,
            arrows: [],
            groups: [],
            regions: []
        };
    }

    function createTreeTemplate() {
        return {
            version: 5,
            uid: createUid(),
            title: 'Karar ağacı',
            nodes: [
                { id: 'n1', label: 'Ana karar', shape: 'decision', tone: 'gold', x: 480, y: 105 },
                { id: 'n2', label: 'Birinci yol', shape: 'process', tone: 'green', x: 260, y: 275 },
                { id: 'n3', label: 'İkinci yol', shape: 'process', tone: 'blue', x: 700, y: 275 },
                { id: 'n4', label: 'Sonuç A', shape: 'terminal', tone: 'neutral', x: 145, y: 440 },
                { id: 'n5', label: 'Sonuç B', shape: 'terminal', tone: 'neutral', x: 375, y: 440 },
                { id: 'n6', label: 'Sonuç C', shape: 'terminal', tone: 'neutral', x: 700, y: 440 }
            ],
            edges: [
                { from: 'n1', to: 'n2', label: 'Evet', style: 'solid' },
                { from: 'n1', to: 'n3', label: 'Hayır', style: 'solid' },
                { from: 'n2', to: 'n4', label: '', style: 'solid' },
                { from: 'n2', to: 'n5', label: '', style: 'solid' },
                { from: 'n3', to: 'n6', label: '', style: 'solid' }
            ],
            arrows: [],
            groups: [],
            regions: []
        };
    }

    function createTimelineTemplate() {
        return {
            version: 5,
            uid: createUid(),
            title: 'Zaman çizelgesi',
            nodes: [
                { id: 'n1', label: 'Başlangıç', shape: 'terminal', tone: 'green', x: 130, y: 270 },
                { id: 'n2', label: 'Birinci aşama', shape: 'process', tone: 'blue', x: 365, y: 270 },
                { id: 'n3', label: 'İkinci aşama', shape: 'process', tone: 'gold', x: 600, y: 270 },
                { id: 'n4', label: 'Tamamlandı', shape: 'terminal', tone: 'green', x: 835, y: 270 }
            ],
            edges: [
                { from: 'n1', to: 'n2', label: '', style: 'solid' },
                { from: 'n2', to: 'n3', label: '', style: 'solid' },
                { from: 'n3', to: 'n4', label: '', style: 'solid' }
            ],
            arrows: [],
            groups: [],
            regions: []
        };
    }

    function createPyramidTemplate() {
        return {
            version: 5,
            uid: createUid(),
            title: 'Katmanlı piramit',
            nodes: [
                { id: 'n1', label: 'Zirve', shape: 'pyramid', tone: 'gold', x: 480, y: 115, width: 230, height: 78 },
                { id: 'n2', label: 'İkinci katman', shape: 'pyramid', tone: 'green', x: 480, y: 210, width: 340, height: 84 },
                { id: 'n3', label: 'Üçüncü katman', shape: 'pyramid', tone: 'blue', x: 480, y: 310, width: 460, height: 90 },
                { id: 'n4', label: 'Temel', shape: 'pyramid', tone: 'neutral', x: 480, y: 420, width: 590, height: 98 }
            ],
            edges: [],
            arrows: [],
            groups: [],
            regions: []
        };
    }

    function createSetsTemplate() {
        return {
            version: 5,
            uid: createUid(),
            title: 'Kümeler ve kesişimler',
            nodes: [
                { id: 'n1', label: 'A', shape: 'set', tone: 'green', x: 285, y: 270, width: 300, height: 250 },
                { id: 'n2', label: 'B', shape: 'set', tone: 'blue', x: 465, y: 270, width: 300, height: 250 },
                { id: 'n3', label: 'C', shape: 'set', tone: 'gold', x: 770, y: 270, width: 230, height: 210 }
            ],
            edges: [],
            arrows: [],
            groups: [],
            regions: [
                { id: 'r1', label: '', operation: 'intersection', tone: 'gold', nodeIds: ['n1', 'n2'] }
            ]
        };
    }

    function cloneGraph(value) {
        return JSON.parse(JSON.stringify(value));
    }

    function defaultNodeLabel(shape) {
        if (shape === 'set') return '';
        if (shape === 'label') return 'Bölge etiketi';
        return 'Adım';
    }

    function normalizeGraphForEditor(value) {
        if (value && Array.isArray(value.n)) {
            value = {
                version: value.v || 2,
                uid: value.i || '',
                title: value.t || 'Diyagram',
                nodes: value.n
                    .filter((node) => Array.isArray(node) && node.length >= 6)
                    .map((node) => ({
                        id: node[0],
                        label: node[1],
                        shape: node[2],
                        tone: node[3],
                        x: node[4],
                        y: node[5],
                        width: node[6],
                        height: node[7],
                        href: node[8],
                        fontSize: node[9],
                        labelOffsetX: node[10],
                        labelOffsetY: node[11]
                    })),
                edges: Array.isArray(value.e)
                    ? value.e
                        .filter((edge) => Array.isArray(edge) && edge.length >= 4)
                        .map((edge) => ({
                            from: edge[0],
                            to: edge[1],
                            label: edge[2],
                            style: edge[3],
                            description: edge[4],
                            route: edge[5],
                            bend: edge[6]
                        }))
                    : [],
                arrows: Array.isArray(value.a)
                    ? value.a
                        .filter((arrow) => Array.isArray(arrow) && arrow.length >= 5)
                        .map((arrow) => ({
                            id: arrow[0],
                            startX: arrow[1],
                            startY: arrow[2],
                            endX: arrow[3],
                            endY: arrow[4],
                            label: arrow[5],
                            style: arrow[6],
                            description: arrow[7],
                            route: arrow[8],
                            bend: arrow[9],
                            startAnchor: arrow[10],
                            endAnchor: arrow[11]
                        }))
                    : [],
                groups: Array.isArray(value.g)
                    ? value.g
                        .filter((group) => Array.isArray(group) && group.length >= 4)
                        .map((group) => ({ id: group[0], label: group[1], tone: group[2], nodeIds: group[3] }))
                    : [],
                regions: Array.isArray(value.r)
                    ? value.r
                        .filter((region) => Array.isArray(region) && region.length >= 5)
                        .map((region) => ({
                            id: region[0],
                            label: region[1],
                            operation: region[2],
                            tone: region[3],
                            nodeIds: region[4],
                            labelOffsetX: region[5],
                            labelOffsetY: region[6]
                        }))
                    : []
            };
        }
        if (!value || !Array.isArray(value.nodes) || !Array.isArray(value.edges)) return null;
        const allowedShapes = new Set(['terminal', 'process', 'decision', 'data', 'document', 'pyramid', 'set', 'label']);
        const allowedTones = new Set(['neutral', 'green', 'blue', 'gold', 'red']);
        const graphValue = cloneGraph(value);
        const allowedRoutes = new Set(['auto', 'straight', 'curve', 'orthogonal']);
        graphValue.version = 5;
        graphValue.uid = /^[A-Za-z0-9_-]{1,32}$/.test(String(graphValue.uid || ''))
            ? String(graphValue.uid)
            : createUid();
        graphValue.title = String(graphValue.title || 'Diyagram').trim().slice(0, 80) || 'Diyagram';
        graphValue.nodes = graphValue.nodes.slice(0, MAX_NODES).map((node, index) => {
            const shape = allowedShapes.has(node.shape) ? node.shape : 'process';
            const fallbackLabel = defaultNodeLabel(shape);
            const label = String(node.label ?? fallbackLabel).trim().slice(0, 240);
            const rawLabelOffsetX = Number(node.labelOffsetX ?? node.label_offset_x ?? 0);
            const rawLabelOffsetY = Number(node.labelOffsetY ?? node.label_offset_y ?? 0);
            const normalizedNode = {
                id: String(node.id || `n${index + 1}`).slice(0, 32),
                label: label || fallbackLabel,
                shape,
                tone: allowedTones.has(node.tone) ? node.tone : 'neutral',
                x: Number(node.x) || 480,
                y: Number(node.y) || 270,
                width: Math.min(MAX_NODE_WIDTH, Math.max(MIN_NODE_WIDTH, Number(node.width) || 152)),
                height: Math.min(MAX_NODE_HEIGHT, Math.max(MIN_NODE_HEIGHT, Number(node.height) || (shape === 'decision' ? 104 : 68))),
                href: normalizeNodeHref(node.href),
                fontSize: Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, Number(node.fontSize) || (shape === 'label' ? 17 : 15))),
                labelOffsetX: Number.isFinite(rawLabelOffsetX) ? rawLabelOffsetX : 0,
                labelOffsetY: Number.isFinite(rawLabelOffsetY) ? rawLabelOffsetY : 0
            };
            const constrainedOffset = constrainNodeLabelOffset(
                normalizedNode,
                normalizedNode.labelOffsetX,
                normalizedNode.labelOffsetY
            );
            normalizedNode.labelOffsetX = constrainedOffset.x;
            normalizedNode.labelOffsetY = constrainedOffset.y;
            return normalizedNode;
        });
        const reservedNodeIds = new Set(graphValue.nodes.map((node) => node.id));
        const seenNodeIds = new Set();
        const numericNodeIds = graphValue.nodes
            .map((node) => /^n(\d+)$/.exec(node.id))
            .filter(Boolean)
            .map((match) => Number(match[1]));
        let repairNodeNumber = Math.max(9, ...numericNodeIds, 0) + 1;
        graphValue.nodes.forEach((node) => {
            if (!seenNodeIds.has(node.id)) {
                seenNodeIds.add(node.id);
                return;
            }
            let replacement = `n${repairNodeNumber}`;
            while (reservedNodeIds.has(replacement) || seenNodeIds.has(replacement)) {
                repairNodeNumber += 1;
                replacement = `n${repairNodeNumber}`;
            }
            node.id = replacement;
            reservedNodeIds.add(replacement);
            seenNodeIds.add(replacement);
            repairNodeNumber += 1;
        });
        graphValue.nodes.forEach((node) => {
            node.x = Math.min(WORLD_WIDTH - (node.width / 2) - 8, Math.max((node.width / 2) + 8, node.x));
            node.y = Math.min(WORLD_HEIGHT - (node.height / 2) - 8, Math.max((node.height / 2) + 8, node.y));
            normalizeNodeLabelOffset(node);
        });
        const nodeIds = new Set(graphValue.nodes.map((node) => node.id));
        const edgePairs = new Set();
        graphValue.edges = graphValue.edges.slice(0, MAX_EDGES).flatMap((edge) => {
            const from = String(edge.from || '').slice(0, 32);
            const to = String(edge.to || '').slice(0, 32);
            const pair = `${from}:${to}`;
            if (!nodeIds.has(from) || !nodeIds.has(to) || edgePairs.has(pair)) return [];
            edgePairs.add(pair);
            return [{
                from,
                to,
                label: String(edge.label || '').trim().slice(0, 50),
                style: edge.style === 'dashed' ? 'dashed' : 'solid',
                description: String(edge.description || '').trim().slice(0, 600),
                route: allowedRoutes.has(edge.route) ? edge.route : 'auto',
                bend: Math.min(MAX_EDGE_BEND, Math.max(-MAX_EDGE_BEND, Number(edge.bend) || 0))
            }];
        });
        const arrowIds = new Set();
        graphValue.arrows = (Array.isArray(graphValue.arrows) ? graphValue.arrows : [])
            .slice(0, MAX_FREE_ARROWS)
            .flatMap((arrow, index) => {
                let id = /^[A-Za-z0-9_-]{1,32}$/.test(String(arrow.id || ''))
                    ? String(arrow.id)
                    : `a${index + 1}`;
                if (arrowIds.has(id)) id = `a${index + 1}-${Date.now().toString(36).slice(-4)}`;
                arrowIds.add(id);
                const startX = Number(arrow.startX);
                const startY = Number(arrow.startY);
                const endX = Number(arrow.endX);
                const endY = Number(arrow.endY);
                if (![startX, startY, endX, endY].every(Number.isFinite)) return [];
                return [{
                    id,
                    startX: Math.min(WORLD_WIDTH - 8, Math.max(8, startX)),
                    startY: Math.min(WORLD_HEIGHT - 8, Math.max(8, startY)),
                    endX: Math.min(WORLD_WIDTH - 8, Math.max(8, endX)),
                    endY: Math.min(WORLD_HEIGHT - 8, Math.max(8, endY)),
                    label: String(arrow.label || '').trim().slice(0, 50),
                    style: arrow.style === 'dashed' ? 'dashed' : 'solid',
                    description: String(arrow.description || '').trim().slice(0, 600),
                    route: allowedRoutes.has(arrow.route) ? arrow.route : 'straight',
                    bend: Math.min(MAX_EDGE_BEND, Math.max(-MAX_EDGE_BEND, Number(arrow.bend) || 0)),
                    startAnchor: String(arrow.startAnchor || arrow.start_anchor || '').slice(0, 35),
                    endAnchor: String(arrow.endAnchor || arrow.end_anchor || '').slice(0, 35)
                }];
            });
        const groupedIds = new Set();
        graphValue.groups = (Array.isArray(graphValue.groups) ? graphValue.groups : [])
            .slice(0, MAX_GROUPS)
            .flatMap((group, index) => {
                const memberIds = (Array.isArray(group.nodeIds) ? group.nodeIds : group.node_ids || [])
                    .map(String)
                    .filter((id) => nodeIds.has(id) && !groupedIds.has(id));
                if (memberIds.length < 2) return [];
                memberIds.forEach((id) => groupedIds.add(id));
                return [{
                    id: /^[A-Za-z0-9_-]{1,32}$/.test(String(group.id || '')) ? String(group.id) : `g${index + 1}`,
                    label: String(group.label || 'Grup').trim().slice(0, 80) || 'Grup',
                    tone: allowedTones.has(group.tone) ? group.tone : 'neutral',
                    nodeIds: memberIds
                }];
            });
        const allowedRegionOperations = new Set(['intersection', 'union', 'difference']);
        const regionIds = new Set();
        graphValue.regions = (Array.isArray(graphValue.regions) ? graphValue.regions : [])
            .slice(0, MAX_REGIONS)
            .flatMap((region, index) => {
                const memberIds = Array.from(new Set(
                    (Array.isArray(region.nodeIds) ? region.nodeIds : region.node_ids || [])
                        .map(String)
                        .filter((id) => nodeIds.has(id))
                ));
                if (memberIds.length < 2) return [];
                let id = /^[A-Za-z0-9_-]{1,32}$/.test(String(region.id || ''))
                    ? String(region.id)
                    : `r${index + 1}`;
                if (regionIds.has(id)) id = `r${index + 1}-${Date.now().toString(36).slice(-4)}`;
                regionIds.add(id);
                const rawLabelOffsetX = Number(region.labelOffsetX ?? region.label_offset_x ?? 0);
                const rawLabelOffsetY = Number(region.labelOffsetY ?? region.label_offset_y ?? 0);
                return [{
                    id,
                    label: String(region.label || '').trim().slice(0, 80),
                    operation: allowedRegionOperations.has(region.operation) ? region.operation : 'intersection',
                    tone: allowedTones.has(region.tone) ? region.tone : 'gold',
                    nodeIds: memberIds,
                    labelOffsetX: Number.isFinite(rawLabelOffsetX)
                        ? Math.min(WORLD_WIDTH, Math.max(-WORLD_WIDTH, rawLabelOffsetX))
                        : 0,
                    labelOffsetY: Number.isFinite(rawLabelOffsetY)
                        ? Math.min(WORLD_HEIGHT, Math.max(-WORLD_HEIGHT, rawLabelOffsetY))
                        : 0
                }];
            });
        const validAnchors = new Set([
            ...Array.from(nodeIds, (id) => `n:${id}`),
            ...Array.from(regionIds, (id) => `r:${id}`)
        ]);
        graphValue.arrows.forEach((arrow) => {
            if (!validAnchors.has(arrow.startAnchor)) arrow.startAnchor = '';
            if (!validAnchors.has(arrow.endAnchor)) arrow.endAnchor = '';
        });
        return graphValue;
    }

    function normalizeNodeHref(value) {
        const href = String(value || '').trim().slice(0, 500);
        if (!href) return '';
        if (href.startsWith('/') && !href.startsWith('//')) return href;
        const candidate = /^[\w.-]+\.[A-Za-z]{2,}(?:[/?#].*)?$/.test(href) ? `https://${href}` : href;
        try {
            const parsed = new URL(candidate);
            return ['http:', 'https:'].includes(parsed.protocol) ? candidate : '';
        } catch (error) {
            return '';
        }
    }

    function openDiagramHref(value) {
        const href = normalizeNodeHref(value);
        if (!href) return false;
        const destination = href.startsWith('/')
            ? new URL(href, window.location.origin).href
            : href;
        const link = document.createElement('a');
        link.href = destination;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.hidden = true;
        document.body.appendChild(link);
        link.click();
        link.remove();
        return true;
    }

    function packGraph(value) {
        return {
            v: 5,
            i: value.uid,
            t: value.title,
            n: value.nodes.map((node) => [
                node.id, node.label, node.shape, node.tone, node.x, node.y,
                node.width, node.height, node.href, node.fontSize,
                node.labelOffsetX || 0, node.labelOffsetY || 0
            ]),
            e: value.edges.map((edge) => [
                edge.from, edge.to, edge.label, edge.style,
                edge.description, edge.route, edge.bend
            ]),
            a: (value.arrows || []).map((arrow) => [
                arrow.id, arrow.startX, arrow.startY, arrow.endX, arrow.endY,
                arrow.label, arrow.style, arrow.description, arrow.route, arrow.bend,
                arrow.startAnchor || '', arrow.endAnchor || ''
            ]),
            g: value.groups.map((group) => [group.id, group.label, group.tone, group.nodeIds]),
            r: value.regions.map((region) => [
                region.id, region.label, region.operation, region.tone, region.nodeIds,
                region.labelOffsetX || 0, region.labelOffsetY || 0
            ])
        };
    }

    function utf8Base64UrlDecode(value) {
        try {
            const padding = '='.repeat((4 - (value.length % 4)) % 4);
            const binary = atob(value.replace(/-/g, '+').replace(/_/g, '/') + padding);
            const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
            return new TextDecoder().decode(bytes);
        } catch (error) {
            return null;
        }
    }

    function findDiagramMarkers(textarea) {
        if (!textarea) return null;
        const value = textarea.value || '';
        const regex = new RegExp(DIAGRAM_MARKER_REGEX.source, 'g');
        const markers = [];
        let match;
        while ((match = regex.exec(value)) !== null) {
            const start = match.index;
            const end = start + match[0].length;
            const decoded = utf8Base64UrlDecode(match[1]);
            if (!decoded) continue;
            try {
                const normalized = normalizeGraphForEditor(JSON.parse(decoded));
                if (normalized) markers.push({ start, end, encoded: match[1], marker: match[0], graph: normalized });
            } catch (error) {
                // A malformed marker must not prevent later valid diagrams from opening.
            }
        }
        return markers;
    }

    function findDiagramMarker(textarea, encodedHint) {
        if (!textarea) return null;
        const selectionStart = textarea.selectionStart || 0;
        const selectionEnd = textarea.selectionEnd || selectionStart;
        return (findDiagramMarkers(textarea) || []).find((marker) => {
            const selectedMarker = selectionStart === selectionEnd
                ? selectionStart >= marker.start && selectionStart <= marker.end
                : selectionStart < marker.end && selectionEnd > marker.start;
            const immediatelyBeforeCaret = selectionStart === selectionEnd
                && selectionStart >= marker.end
                && selectionStart - marker.end <= 2
                && /^\s*$/.test(textarea.value.slice(marker.end, selectionStart));
            return encodedHint === marker.encoded || selectedMarker || immediatelyBeforeCaret;
        }) || null;
    }

    function loadGraph(value, marker) {
        const normalized = normalizeGraphForEditor(value);
        if (!normalized) return false;
        graph = normalized;
        editingMarker = marker || null;
        history = [];
        redoHistory = [];
        selected = null;
        selectedNodeIds.clear();
        disableConnectMode(false);
        syncNextNodeNumber();
        titleInput.value = graph.title;
        editorTitle.textContent = editingMarker ? 'Diyagramı düzenle' : 'Akışı oluştur';
        insertButton.innerHTML = editingMarker
            ? '<i class="bi bi-check-lg" aria-hidden="true"></i> Diyagramı güncelle'
            : '<i class="bi bi-plus-lg" aria-hidden="true"></i> Metne ekle';
        document.querySelectorAll('[data-diagram-template]').forEach((button) => {
            button.classList.remove('active');
        });
        resetView();
        setStatus(editingMarker ? 'Mevcut diyagram düzenlemeye açıldı' : 'Diyagram hazır');
        render();
        return true;
    }

    function pushHistory() {
        history.push(JSON.stringify(graph));
        if (history.length > 30) history.shift();
        redoHistory = [];
    }

    function setStatus(message) {
        status.textContent = message;
    }

    function resetView() {
        viewState = { zoom: 1, panX: 0, panY: 0 };
        applyViewport();
    }

    function clampZoom(value) {
        return Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, value));
    }

    function applyViewport() {
        viewportLayer.setAttribute(
            'transform',
            `translate(${viewState.panX} ${viewState.panY}) scale(${viewState.zoom})`
        );
        zoomValue.textContent = `%${Math.round(viewState.zoom * 100)}`;
        canvas.classList.toggle('space-pan-active', spacePanActive);
        renderMiniMapViewport();
    }

    function rootCanvasPoint(event) {
        const point = canvas.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        const matrix = canvas.getScreenCTM();
        return matrix ? point.matrixTransform(matrix.inverse()) : { x: 480, y: 270 };
    }

    function canvasPoint(event) {
        const point = rootCanvasPoint(event);
        return {
            x: (point.x - viewState.panX) / viewState.zoom,
            y: (point.y - viewState.panY) / viewState.zoom
        };
    }

    function zoomAt(nextZoom, anchor) {
        const oldZoom = viewState.zoom;
        const zoom = clampZoom(nextZoom);
        if (Math.abs(zoom - oldZoom) < 0.001) return;
        const point = anchor || { x: VIEWPORT_WIDTH / 2, y: VIEWPORT_HEIGHT / 2 };
        const contentX = (point.x - viewState.panX) / oldZoom;
        const contentY = (point.y - viewState.panY) / oldZoom;
        viewState.zoom = zoom;
        viewState.panX = point.x - (contentX * zoom);
        viewState.panY = point.y - (contentY * zoom);
        applyViewport();
    }

    function fitGraph() {
        const freeArrows = graph.arrows || [];
        if (!graph.nodes.length && !freeArrows.length) {
            resetView();
            return;
        }
        const xs = graph.nodes.flatMap((node) => [node.x - (node.width / 2), node.x + (node.width / 2)]);
        const ys = graph.nodes.flatMap((node) => [node.y - (node.height / 2), node.y + (node.height / 2)]);
        freeArrows.forEach((arrow) => {
            const geometry = freeArrowGeometry(arrow);
            xs.push(arrow.startX, arrow.endX, geometry.handleX);
            ys.push(arrow.startY, arrow.endY, geometry.handleY);
        });
        const left = Math.min(...xs) - 50;
        const right = Math.max(...xs) + 50;
        const top = Math.min(...ys) - 50;
        const bottom = Math.max(...ys) + 50;
        const width = Math.max(1, right - left);
        const height = Math.max(1, bottom - top);
        const zoom = clampZoom(Math.min(900 / width, 480 / height, 1.35));
        viewState.zoom = zoom;
        viewState.panX = (VIEWPORT_WIDTH / 2) - (((left + right) / 2) * zoom);
        viewState.panY = (VIEWPORT_HEIGHT / 2) - (((top + bottom) / 2) * zoom);
        applyViewport();
        setStatus('Diyagram çalışma alanına sığdırıldı');
    }

    function renderMiniMapViewport() {
        if (!miniMapViewport) return;
        miniMapViewport.setAttribute('x', String(-viewState.panX / viewState.zoom));
        miniMapViewport.setAttribute('y', String(-viewState.panY / viewState.zoom));
        miniMapViewport.setAttribute('width', String(VIEWPORT_WIDTH / viewState.zoom));
        miniMapViewport.setAttribute('height', String(VIEWPORT_HEIGHT / viewState.zoom));
    }

    function renderMiniMap() {
        if (!miniMapContent) return;
        miniMapContent.replaceChildren();
        const nodeMap = new Map(graph.nodes.map((node) => [node.id, node]));
        graph.edges.forEach((edge) => {
            const source = nodeMap.get(edge.from);
            const target = nodeMap.get(edge.to);
            if (!source || !target) return;
            miniMapContent.appendChild(svgElement('line', {
                x1: source.x,
                y1: source.y,
                x2: target.x,
                y2: target.y,
                class: 'diagram-minimap-edge'
            }));
        });
        (graph.arrows || []).forEach((arrow) => {
            miniMapContent.appendChild(svgElement('path', {
                d: freeArrowGeometry(arrow).path,
                class: 'diagram-minimap-edge',
                fill: 'none'
            }));
        });
        graph.nodes.forEach((node) => {
            miniMapContent.appendChild(svgElement('rect', {
                x: node.x - (node.width / 2),
                y: node.y - (node.height / 2),
                width: node.width,
                height: node.height,
                rx: 7,
                class: `diagram-minimap-node diagram-minimap-node-${node.tone || 'neutral'}`
            }));
        });
        renderMiniMapViewport();
    }

    function graphStorageKey() {
        return `hafif-diagram-versions:${graph.uid || 'draft'}`;
    }

    function getLocalVersions() {
        try {
            const value = JSON.parse(localStorage.getItem(graphStorageKey()) || '[]');
            return Array.isArray(value) ? value : [];
        } catch (error) {
            return [];
        }
    }

    function saveLocalVersion(label) {
        if (!graph || !graph.nodes) return;
        try {
            const versions = getLocalVersions();
            const serialized = JSON.stringify(packGraph(graph));
            if (versions[0] && versions[0].graph === serialized) return;
            versions.unshift({
                id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
                savedAt: new Date().toISOString(),
                label: label || 'Kaydedilmiş sürüm',
                graph: serialized
            });
            localStorage.setItem(graphStorageKey(), JSON.stringify(versions.slice(0, 8)));
        } catch (error) {
            // Storage errors must never block the editor.
        }
    }

    function renderVersionList() {
        versionList.replaceChildren();
        const versions = getLocalVersions();
        if (!versions.length) {
            const empty = document.createElement('p');
            empty.className = 'diagram-version-empty';
            empty.textContent = 'Henüz kaydedilmiş sürüm yok.';
            versionList.appendChild(empty);
            return;
        }
        versions.forEach((version) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'diagram-version-item';
            const date = new Date(version.savedAt);
            const label = document.createElement('strong');
            const timestamp = document.createElement('span');
            label.textContent = version.label || 'Kaydedilmiş sürüm';
            timestamp.textContent = Number.isNaN(date.getTime()) ? '' : date.toLocaleString('tr-TR');
            button.append(label, timestamp);
            button.addEventListener('click', () => {
                try {
                    const restored = normalizeGraphForEditor(JSON.parse(version.graph));
                    if (!restored) return;
                    history.push(JSON.stringify(graph));
                    graph = restored;
                    syncNextNodeNumber();
                    titleInput.value = graph.title;
                    selected = null;
                    selectedNodeIds.clear();
                    setStatus('Kaydedilmiş sürüm geri yüklendi');
                    render();
                } catch (error) {
                    setStatus('Bu sürüm geri yüklenemedi');
                }
            });
            versionList.appendChild(button);
        });
    }

    function selectTemplate(name) {
        let template = createCycleTemplate();
        if (name === 'blank') template = createBlankTemplate();
        if (name === 'flow') template = createFlowTemplate();
        if (name === 'tree') template = createTreeTemplate();
        if (name === 'timeline') template = createTimelineTemplate();
        if (name === 'pyramid') template = createPyramidTemplate();
        if (name === 'sets') template = createSetsTemplate();
        if (name === 'spiral') template = createSpiralTemplate();
        graph = normalizeGraphForEditor(template);
        syncNextNodeNumber();
        history = [];
        redoHistory = [];
        selected = null;
        selectedNodeIds.clear();
        disableConnectMode();
        resetView();
        titleInput.value = graph.title;
        document.querySelectorAll('[data-diagram-template]').forEach((button) => {
            button.classList.toggle('active', button.dataset.diagramTemplate === name);
        });
        setStatus(name === 'blank' ? 'Boş tuval hazır' : `${graph.title} taslağı hazır`);
        render();
    }

    function nodeDimensions(node) {
        return { halfWidth: node.width / 2, halfHeight: node.height / 2 };
    }

    function boundaryPoint(node, other) {
        const dx = other.x - node.x;
        const dy = other.y - node.y;
        if (!dx && !dy) return { x: node.x, y: node.y };
        const dimensions = nodeDimensions(node);
        if (node.shape === 'set') {
            const denominator = Math.sqrt(
                ((dx / dimensions.halfWidth) ** 2) + ((dy / dimensions.halfHeight) ** 2)
            );
            const scale = denominator ? 1 / denominator : 0;
            return { x: node.x + (dx * scale), y: node.y + (dy * scale) };
        }
        if (node.shape === 'decision') {
            const denominator = (Math.abs(dx) / dimensions.halfWidth)
                + (Math.abs(dy) / dimensions.halfHeight);
            const scale = denominator ? 1 / denominator : 0;
            return { x: node.x + (dx * scale), y: node.y + (dy * scale) };
        }
        const scaleX = dx ? dimensions.halfWidth / Math.abs(dx) : Infinity;
        const scaleY = dy ? dimensions.halfHeight / Math.abs(dy) : Infinity;
        const scale = Math.min(scaleX, scaleY);
        return { x: node.x + dx * scale, y: node.y + dy * scale };
    }

    function pointInsideNode(point, node) {
        const dimensions = nodeDimensions(node);
        const dx = point.x - node.x;
        const dy = point.y - node.y;
        if (node.shape === 'set') {
            return ((dx / dimensions.halfWidth) ** 2) + ((dy / dimensions.halfHeight) ** 2) <= 1;
        }
        if (node.shape === 'decision') {
            return (Math.abs(dx) / dimensions.halfWidth) + (Math.abs(dy) / dimensions.halfHeight) <= 1;
        }
        return Math.abs(dx) <= dimensions.halfWidth && Math.abs(dy) <= dimensions.halfHeight;
    }

    function pointInsideRegion(point, region, members) {
        if (members.length < 2) return false;
        const membership = members.map((node) => pointInsideNode(point, node));
        if (region.operation === 'union') return membership.some(Boolean);
        if (region.operation === 'difference') return membership[0] && !membership.slice(1).some(Boolean);
        return membership.every(Boolean);
    }

    function regionInteriorPoints(region, members, bounds, steps = 10) {
        const candidates = members.map((node) => ({ x: node.x, y: node.y }));
        for (let row = 0; row <= steps; row += 1) {
            for (let column = 0; column <= steps; column += 1) {
                candidates.push({
                    x: bounds.left + ((bounds.right - bounds.left) * (column / steps)),
                    y: bounds.top + ((bounds.bottom - bounds.top) * (row / steps))
                });
            }
        }
        return candidates.filter((point) => pointInsideRegion(point, region, members));
    }

    function regionAnchorPoint(region, members, bounds, target = null) {
        const reference = target || {
            x: (bounds.left + bounds.right) / 2,
            y: (bounds.top + bounds.bottom) / 2
        };
        return regionInteriorPoints(region, members, bounds).reduce((closest, point) => {
            const distance = Math.hypot(point.x - reference.x, point.y - reference.y);
            return !closest || distance < closest.distance ? { point, distance } : closest;
        }, null)?.point || null;
    }

    function distanceToNearbyRegion(point, region, members, bounds, tolerance) {
        if (pointInsideRegion(point, region, members)) return 0;
        if (
            point.x < bounds.left - tolerance
            || point.x > bounds.right + tolerance
            || point.y < bounds.top - tolerance
            || point.y > bounds.bottom + tolerance
        ) return Infinity;
        const ringCount = 7;
        const angleCount = 28;
        for (let ring = 1; ring <= ringCount; ring += 1) {
            const radius = tolerance * (ring / ringCount);
            for (let angleIndex = 0; angleIndex < angleCount; angleIndex += 1) {
                const angle = (Math.PI * 2 * angleIndex) / angleCount;
                const candidate = {
                    x: point.x + (Math.cos(angle) * radius),
                    y: point.y + (Math.sin(angle) * radius)
                };
                if (pointInsideRegion(candidate, region, members)) return radius;
            }
        }
        return Infinity;
    }

    function resolveArrowAnchor(anchor) {
        const match = /^([nr]):([A-Za-z0-9_-]{1,32})$/.exec(String(anchor || ''));
        if (!match) return null;
        if (match[1] === 'n') {
            const node = graph.nodes.find((item) => item.id === match[2]);
            if (!node) return null;
            return { type: 'node', node, center: { x: node.x, y: node.y } };
        }
        const region = graph.regions.find((item) => item.id === match[2]);
        if (!region) return null;
        const members = regionMembers(region);
        const bounds = regionBounds(region, members);
        if (!bounds) return null;
        const center = regionAnchorPoint(region, members, bounds);
        if (!center) return null;
        return {
            type: 'region',
            region,
            members,
            bounds,
            center
        };
    }

    function arrowAnchorLabel(anchor) {
        if (!anchor) return 'Serbest';
        const match = /^([nr]):([A-Za-z0-9_-]{1,32})$/.exec(String(anchor));
        if (!match) return 'Serbest';
        if (match[1] === 'n') {
            const node = graph.nodes.find((item) => item.id === match[2]);
            return node ? `Şekil · ${node.label || 'Adsız şekil'}` : 'Serbest';
        }
        const region = graph.regions.find((item) => item.id === match[2]);
        if (!region) return 'Serbest';
        const name = region.label || `${regionOperationSymbol(region.operation)} bölgesi`;
        return regionBounds(region, regionMembers(region)) ? `Bölge · ${name}` : `Bölge · ${name} (kesişim yok)`;
    }

    function findArrowAnchorAtPoint(point) {
        const tolerance = Math.min(180, Math.max(8, ARROW_REGION_SNAP_PX / viewState.zoom));
        const regionCandidates = graph.regions
            .map((region) => ({ region, members: regionMembers(region) }))
            .map((candidate) => ({ ...candidate, bounds: regionBounds(candidate.region, candidate.members) }))
            .filter((candidate) => candidate.bounds)
            .map((candidate) => ({
                ...candidate,
                distance: distanceToNearbyRegion(
                    point,
                    candidate.region,
                    candidate.members,
                    candidate.bounds,
                    tolerance
                )
            }))
            .filter((candidate) => Number.isFinite(candidate.distance))
            .sort((a, b) => (
                a.distance - b.distance
                || ((a.bounds.right - a.bounds.left) * (a.bounds.bottom - a.bounds.top))
                - ((b.bounds.right - b.bounds.left) * (b.bounds.bottom - b.bounds.top))
            ));
        if (regionCandidates.length) return `r:${regionCandidates[0].region.id}`;
        const node = [...graph.nodes].reverse().find((item) => pointInsideNode(point, item));
        return node ? `n:${node.id}` : '';
    }

    function setArrowDropTarget(anchor) {
        if (anchor === freeArrowDropAnchor) return;
        freeArrowDropAnchor = anchor || '';
        nodesLayer.querySelectorAll('.is-arrow-drop-target').forEach((element) => {
            element.classList.remove('is-arrow-drop-target');
        });
        regionsLayer.querySelectorAll('.is-arrow-drop-target').forEach((element) => {
            element.classList.remove('is-arrow-drop-target');
        });
        if (!freeArrowDropAnchor) return;
        const match = /^([nr]):([A-Za-z0-9_-]{1,32})$/.exec(freeArrowDropAnchor);
        if (!match) return;
        const layer = match[1] === 'r' ? regionsLayer : nodesLayer;
        const dataKey = match[1] === 'r' ? 'regionId' : 'nodeId';
        const target = Array.from(layer.children).find((element) => element.dataset[dataKey] === match[2]);
        if (target) target.classList.add('is-arrow-drop-target');
    }

    function resolvedFreeArrowEndpoints(arrow) {
        const rawStart = { x: arrow.startX, y: arrow.startY };
        const rawEnd = { x: arrow.endX, y: arrow.endY };
        const startAnchor = resolveArrowAnchor(arrow.startAnchor);
        const endAnchor = resolveArrowAnchor(arrow.endAnchor);
        const start = startAnchor ? startAnchor.center : rawStart;
        const end = endAnchor ? endAnchor.center : rawEnd;
        return { start, end, startAnchor, endAnchor };
    }

    function lineCrossesNode(start, end, node) {
        const dimensions = nodeDimensions(node);
        for (let step = 1; step < 20; step += 1) {
            const ratio = step / 20;
            const x = start.x + ((end.x - start.x) * ratio);
            const y = start.y + ((end.y - start.y) * ratio);
            if (
                Math.abs(x - node.x) <= dimensions.halfWidth + 18
                && Math.abs(y - node.y) <= dimensions.halfHeight + 18
            ) return true;
        }
        return false;
    }

    function connectorGeometry(start, end, connector, resolvedRoute, reverseBend) {
        if (resolvedRoute === 'straight') {
            return {
                path: `M ${start.x} ${start.y} L ${end.x} ${end.y}`,
                labelX: (start.x + end.x) / 2,
                labelY: (start.y + end.y) / 2 - 10,
                handleX: (start.x + end.x) / 2,
                handleY: (start.y + end.y) / 2,
                resolvedRoute
            };
        }

        if (resolvedRoute === 'orthogonal') {
            const dx = end.x - start.x;
            const dy = end.y - start.y;
            if (Math.abs(dx) >= Math.abs(dy)) {
                const middleX = ((start.x + end.x) / 2) + (connector.bend || 0);
                return {
                    path: `M ${start.x} ${start.y} H ${middleX} V ${end.y} H ${end.x}`,
                    labelX: middleX,
                    labelY: ((start.y + end.y) / 2) - 10,
                    handleX: middleX,
                    handleY: (start.y + end.y) / 2,
                    resolvedRoute,
                    axis: 'x'
                };
            }
            const middleY = ((start.y + end.y) / 2) + (connector.bend || 0);
            return {
                path: `M ${start.x} ${start.y} V ${middleY} H ${end.x} V ${end.y}`,
                labelX: (start.x + end.x) / 2,
                labelY: middleY - 10,
                handleX: (start.x + end.x) / 2,
                handleY: middleY,
                resolvedRoute,
                axis: 'y'
            };
        }

        const dx = end.x - start.x;
        const dy = end.y - start.y;
        const length = Math.max(Math.hypot(dx, dy), 1);
        const bend = Number(connector.bend) || (connector.route === 'curve' ? 0 : (reverseBend ? -48 : 48));
        const controlX = (start.x + end.x) / 2 + (-dy / length) * bend;
        const controlY = (start.y + end.y) / 2 + (dx / length) * bend;
        const curveX = (start.x + (2 * controlX) + end.x) / 4;
        const curveY = (start.y + (2 * controlY) + end.y) / 4;
        return {
            path: `M ${start.x} ${start.y} Q ${controlX} ${controlY} ${end.x} ${end.y}`,
            labelX: curveX,
            labelY: curveY - 8,
            handleX: curveX,
            handleY: curveY,
            resolvedRoute: 'curve'
        };
    }

    function edgeGeometry(source, target, edge, hasReverse, reverseBend) {
        if (source.id === target.id) {
            const dimensions = nodeDimensions(source);
            return {
                path: `M ${source.x + (dimensions.halfWidth * 0.58)} ${source.y - (dimensions.halfHeight * 0.85)} C ${source.x + dimensions.halfWidth + 60} ${source.y - dimensions.halfHeight - 62}, ${source.x - dimensions.halfWidth - 60} ${source.y - dimensions.halfHeight - 62}, ${source.x - (dimensions.halfWidth * 0.58)} ${source.y - (dimensions.halfHeight * 0.85)}`,
                labelX: source.x,
                labelY: source.y - dimensions.halfHeight - 70,
                handleX: source.x,
                handleY: source.y - dimensions.halfHeight - 62,
                resolvedRoute: 'curve'
            };
        }

        const start = boundaryPoint(source, target);
        const end = boundaryPoint(target, source);
        let resolvedRoute = edge.route || 'auto';
        if (resolvedRoute === 'auto') {
            const blocked = graph.nodes.some((node) => (
                ![source.id, target.id].includes(node.id) && lineCrossesNode(start, end, node)
            ));
            resolvedRoute = blocked ? 'orthogonal' : 'straight';
        }
        if (hasReverse && resolvedRoute === 'straight') resolvedRoute = 'curve';
        return connectorGeometry(start, end, edge, resolvedRoute, reverseBend);
    }

    function freeArrowGeometry(arrow) {
        const { start, end } = resolvedFreeArrowEndpoints(arrow);
        const route = arrow.route === 'auto' ? 'straight' : arrow.route;
        return connectorGeometry(start, end, arrow, route, false);
    }

    function wrapLabel(node) {
        const fallbackLabel = defaultNodeLabel(node.shape);
        const label = String(node.label ?? fallbackLabel).trim();
        if (!label) return [];
        const words = label.split(/\s+/);
        const lines = [];
        let line = '';
        const fontSize = Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, Number(node.fontSize) || 15));
        const lineHeight = fontSize * 1.22;
        const maxCharacters = Math.max(5, Math.floor((node.width - 28) / (fontSize * 0.52)));
        const maxLines = Math.max(1, Math.min(20, Math.floor((node.height - 18) / lineHeight)));
        words.forEach((word) => {
            if (!line) {
                line = word;
                return;
            }
            if (`${line} ${word}`.length <= maxCharacters) {
                line += ` ${word}`;
            } else {
                lines.push(line);
                line = word;
            }
        });
        if (line) lines.push(line);
        if (lines.length > maxLines) {
            lines.length = maxLines;
            lines[maxLines - 1] = `${lines[maxLines - 1].slice(0, Math.max(8, maxCharacters - 3)).trim()}...`;
        }
        return lines;
    }

    function nodeLabelMetrics(node) {
        const lines = wrapLabel(node);
        const fontSize = Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, Number(node.fontSize) || 15));
        const lineHeight = fontSize * 1.22;
        const longestLine = Math.max(0, ...lines.map((line) => Array.from(line).length));
        return {
            width: Math.min(Math.max(0, node.width - 18), longestLine * fontSize * 0.56),
            height: lines.length * lineHeight
        };
    }

    function constrainNodeLabelOffset(node, rawX, rawY) {
        const dimensions = nodeDimensions(node);
        const metrics = nodeLabelMetrics(node);
        const radiusX = Math.max(0, dimensions.halfWidth - (metrics.width / 2) - 8);
        const radiusY = Math.max(0, dimensions.halfHeight - (metrics.height / 2) - 7);
        let x = Number.isFinite(Number(rawX)) ? Number(rawX) : 0;
        let y = Number.isFinite(Number(rawY)) ? Number(rawY) : 0;
        x = Math.min(radiusX, Math.max(-radiusX, x));
        y = Math.min(radiusY, Math.max(-radiusY, y));

        if (node.shape === 'set' && radiusX > 0 && radiusY > 0) {
            const distance = Math.sqrt(((x / radiusX) ** 2) + ((y / radiusY) ** 2));
            if (distance > 1) {
                x /= distance;
                y /= distance;
            }
        } else if (node.shape === 'decision' && radiusX > 0 && radiusY > 0) {
            const distance = (Math.abs(x) / radiusX) + (Math.abs(y) / radiusY);
            if (distance > 1) {
                x /= distance;
                y /= distance;
            }
        }
        return { x: Math.round(x * 10) / 10, y: Math.round(y * 10) / 10 };
    }

    function normalizeNodeLabelOffset(node) {
        const offset = constrainNodeLabelOffset(node, node.labelOffsetX, node.labelOffsetY);
        node.labelOffsetX = offset.x;
        node.labelOffsetY = offset.y;
        return offset;
    }

    function edgeLabelWidth(label) {
        return Math.max(48, Math.min(220, Array.from(String(label || '')).length * 7.4 + 24));
    }

    function focusAndSelect(input) {
        window.requestAnimationFrame(() => {
            input.focus();
            input.select();
        });
    }

    function selectedNodes() {
        return graph.nodes.filter((node) => selectedNodeIds.has(node.id));
    }

    function matchingSelectedGroup() {
        if (selectedNodeIds.size < 2) return null;
        return graph.groups.find((group) => (
            group.nodeIds.length === selectedNodeIds.size
            && group.nodeIds.every((id) => selectedNodeIds.has(id))
        )) || null;
    }

    function setSingleNodeSelection(nodeId) {
        selectedNodeIds = new Set([nodeId]);
        selected = { type: 'node', id: nodeId };
    }

    function toggleNodeSelection(nodeId) {
        if (selectedNodeIds.has(nodeId)) selectedNodeIds.delete(nodeId);
        else selectedNodeIds.add(nodeId);
        if (selectedNodeIds.size === 1) {
            const [onlyId] = selectedNodeIds;
            selected = { type: 'node', id: onlyId };
        } else {
            selected = null;
        }
    }

    function selectEdge(index, editLabel) {
        selected = { type: 'edge', index };
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('Bağlantı seçildi');
        render();
        if (editLabel) focusAndSelect(edgeLabelInput);
    }

    function selectFreeArrow(arrowId, editLabel) {
        selected = { type: 'arrow', id: arrowId };
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('Bağımsız ok seçildi');
        render();
        if (editLabel) focusAndSelect(edgeLabelInput);
    }

    function getSelectedConnector() {
        if (!selected) return null;
        if (selected.type === 'edge') {
            const connector = graph.edges[selected.index];
            return connector ? { type: 'edge', connector, index: selected.index } : null;
        }
        if (selected.type === 'arrow') {
            const connector = (graph.arrows || []).find((arrow) => arrow.id === selected.id);
            return connector ? { type: 'arrow', connector, id: selected.id } : null;
        }
        return null;
    }

    function renderConnector(group, connector, geometry, isSelected, selectConnector) {
        const visiblePath = svgElement('path', {
            d: geometry.path,
            class: `diagram-editor-edge${connector.style === 'dashed' ? ' dashed' : ''}${isSelected ? ' selected' : ''}`,
            'marker-end': 'url(#diagramEditorArrow)'
        });
        const hitPath = svgElement('path', { d: geometry.path, class: 'diagram-editor-edge-hit' });
        hitPath.addEventListener('pointerdown', (event) => {
            event.stopPropagation();
            selectConnector(event.detail > 1);
        });
        group.append(visiblePath, hitPath);
        if (!connector.label) return;
        const labelWidth = edgeLabelWidth(connector.label);
        const labelGroup = svgElement('g', {
            class: `diagram-editor-edge-label-group${isSelected ? ' selected' : ''}`
        });
        const labelBackground = svgElement('rect', {
            x: geometry.labelX - (labelWidth / 2),
            y: geometry.labelY - 18,
            width: labelWidth,
            height: 26,
            rx: 13,
            class: 'diagram-editor-edge-label-bg'
        });
        const connectorLabel = svgElement('text', {
            x: geometry.labelX,
            y: geometry.labelY,
            class: 'diagram-editor-edge-label'
        });
        connectorLabel.textContent = connector.label;
        labelGroup.addEventListener('pointerdown', (event) => {
            event.stopPropagation();
            selectConnector(event.detail > 1);
        });
        labelGroup.addEventListener('dblclick', (event) => {
            event.preventDefault();
            event.stopPropagation();
            selectConnector(true);
        });
        labelGroup.append(labelBackground, connectorLabel);
        group.appendChild(labelGroup);
    }

    function renderEdges() {
        edgesLayer.replaceChildren();
        const nodesById = new Map(graph.nodes.map((node) => [node.id, node]));
        const pairs = new Set(graph.edges.map((edge) => `${edge.from}:${edge.to}`));

        graph.edges.forEach((edge, index) => {
            const source = nodesById.get(edge.from);
            const target = nodesById.get(edge.to);
            if (!source || !target) return;
            const hasReverse = source.id !== target.id && pairs.has(`${edge.to}:${edge.from}`);
            const geometry = edgeGeometry(source, target, edge, hasReverse, hasReverse && edge.from > edge.to);

            const group = svgElement('g', { 'data-edge-index': index });
            const isSelected = selected && selected.type === 'edge' && selected.index === index;
            renderConnector(group, edge, geometry, isSelected, (editLabel) => selectEdge(index, editLabel));
            edgesLayer.appendChild(group);
        });

        (graph.arrows || []).forEach((arrow) => {
            const geometry = freeArrowGeometry(arrow);
            const group = svgElement('g', { 'data-free-arrow-id': arrow.id });
            const isSelected = selected && selected.type === 'arrow' && selected.id === arrow.id;
            renderConnector(group, arrow, geometry, isSelected, (editLabel) => selectFreeArrow(arrow.id, editLabel));
            edgesLayer.appendChild(group);
        });
    }

    function groupBounds(group) {
        const members = graph.nodes.filter((node) => group.nodeIds.includes(node.id));
        if (members.length < 2) return null;
        return {
            left: Math.min(...members.map((node) => node.x - (node.width / 2))) - 26,
            top: Math.min(...members.map((node) => node.y - (node.height / 2))) - 42,
            right: Math.max(...members.map((node) => node.x + (node.width / 2))) + 26,
            bottom: Math.max(...members.map((node) => node.y + (node.height / 2))) + 26
        };
    }

    function renderGroups() {
        groupsLayer.replaceChildren();
        graph.groups.forEach((group) => {
            const bounds = groupBounds(group);
            if (!bounds) return;
            const allSelected = group.nodeIds.every((id) => selectedNodeIds.has(id));
            const groupElement = svgElement('g', {
                class: `diagram-editor-group diagram-editor-group-${group.tone || 'neutral'}${allSelected ? ' selected' : ''}`,
                'data-group-id': group.id,
                tabindex: '0'
            });
            const groupRect = svgElement('rect', {
                x: bounds.left,
                y: bounds.top,
                width: bounds.right - bounds.left,
                height: bounds.bottom - bounds.top,
                rx: 14
            });
            const groupText = svgElement('text', { x: bounds.left + 16, y: bounds.top + 25 });
            groupText.textContent = group.label;
            groupElement.append(groupRect, groupText);
            groupElement.addEventListener('pointerdown', (event) => {
                event.stopPropagation();
                selected = null;
                selectedNodeIds = new Set(group.nodeIds);
                disableConnectMode(false);
                setStatus(`${group.label} grubu seçildi`);
                render();
            });
            groupElement.addEventListener('keydown', (event) => {
                if (event.key !== 'Enter' && event.key !== ' ') return;
                event.preventDefault();
                selected = null;
                selectedNodeIds = new Set(group.nodeIds);
                render();
            });
            groupsLayer.appendChild(groupElement);
        });
    }

    function renderNodeShape(node, group, shapeClass) {
        const dimensions = nodeDimensions(node);
        let shapeElement;
        if (node.shape === 'label') {
            shapeElement = svgElement('rect', {
                x: node.x - dimensions.halfWidth,
                y: node.y - dimensions.halfHeight,
                width: node.width,
                height: node.height,
                rx: 6
            });
        } else if (node.shape === 'decision') {
            shapeElement = svgElement('polygon', {
                points: `${node.x},${node.y - dimensions.halfHeight} ${node.x + dimensions.halfWidth},${node.y} ${node.x},${node.y + dimensions.halfHeight} ${node.x - dimensions.halfWidth},${node.y}`
            });
        } else if (node.shape === 'data') {
            const inset = Math.min(18, node.width * 0.1);
            shapeElement = svgElement('polygon', {
                points: `${node.x - dimensions.halfWidth + inset},${node.y - dimensions.halfHeight} ${node.x + dimensions.halfWidth},${node.y - dimensions.halfHeight} ${node.x + dimensions.halfWidth - inset},${node.y + dimensions.halfHeight} ${node.x - dimensions.halfWidth},${node.y + dimensions.halfHeight}`
            });
        } else if (node.shape === 'document') {
            shapeElement = svgElement('path', {
                d: `M ${node.x - dimensions.halfWidth} ${node.y - dimensions.halfHeight} H ${node.x + dimensions.halfWidth} V ${node.y + dimensions.halfHeight - 12} C ${node.x + (dimensions.halfWidth * 0.5)} ${node.y + dimensions.halfHeight - 26}, ${node.x + (dimensions.halfWidth * 0.16)} ${node.y + dimensions.halfHeight + 8}, ${node.x - (dimensions.halfWidth * 0.26)} ${node.y + dimensions.halfHeight - 8} C ${node.x - (dimensions.halfWidth * 0.6)} ${node.y + dimensions.halfHeight - 20}, ${node.x - (dimensions.halfWidth * 0.8)} ${node.y + dimensions.halfHeight}, ${node.x - dimensions.halfWidth} ${node.y + dimensions.halfHeight - 6} Z`
            });
        } else if (node.shape === 'pyramid') {
            const inset = node.width * 0.18;
            shapeElement = svgElement('polygon', {
                points: `${node.x - dimensions.halfWidth + inset},${node.y - dimensions.halfHeight} ${node.x + dimensions.halfWidth - inset},${node.y - dimensions.halfHeight} ${node.x + dimensions.halfWidth},${node.y + dimensions.halfHeight} ${node.x - dimensions.halfWidth},${node.y + dimensions.halfHeight}`
            });
        } else if (node.shape === 'set') {
            shapeElement = svgElement('ellipse', {
                cx: node.x,
                cy: node.y,
                rx: dimensions.halfWidth,
                ry: dimensions.halfHeight
            });
        } else {
            shapeElement = svgElement('rect', {
                x: node.x - dimensions.halfWidth,
                y: node.y - dimensions.halfHeight,
                width: node.width,
                height: node.height,
                rx: node.shape === 'terminal' ? Math.min(dimensions.halfHeight, 34) : 8
            });
        }
        if (shapeClass) shapeElement.setAttribute('class', shapeClass);
        group.appendChild(shapeElement);
        return shapeElement;
    }

    function renderNodes() {
        nodesLayer.replaceChildren();
        const layerPriority = { set: 0, pyramid: 1, label: 3 };
        const orderedNodes = graph.nodes
            .map((node, index) => ({ node, index }))
            .sort((left, right) => (
                (layerPriority[left.node.shape] ?? 2) - (layerPriority[right.node.shape] ?? 2)
                || left.index - right.index
            ))
            .map((item) => item.node);
        orderedNodes.forEach((node) => {
            const isSelected = selectedNodeIds.has(node.id);
            const classes = [
                'diagram-editor-node',
                `diagram-editor-node-${node.shape}`,
                `diagram-editor-tone-${node.tone || 'neutral'}`,
                isSelected ? 'selected' : '',
                connectSource === node.id ? 'connect-source' : ''
            ].filter(Boolean).join(' ');
            const group = svgElement('g', { class: classes, 'data-node-id': node.id, tabindex: '0' });
            renderNodeShape(node, group);

            const lines = wrapLabel(node);
            const fontSize = Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, Number(node.fontSize) || 15));
            const lineHeight = fontSize * 1.22;
            const labelOffset = normalizeNodeLabelOffset(node);
            const labelX = node.x + labelOffset.x;
            const labelY = node.y + labelOffset.y;
            const text = svgElement('text', {
                class: 'diagram-editor-node-label',
                style: `font-size:${fontSize}px`,
                'aria-label': 'Yazıyı şeklin içinde taşımak için sürükle'
            });
            const textTitle = svgElement('title');
            textTitle.textContent = 'Yazıyı şeklin içinde taşımak için sürükle';
            text.appendChild(textTitle);
            const firstY = labelY - ((lines.length - 1) * lineHeight / 2);
            lines.forEach((line, index) => {
                const tspan = svgElement('tspan', { x: labelX, y: firstY + index * lineHeight });
                tspan.textContent = line;
                text.appendChild(tspan);
            });
            text.addEventListener('pointerdown', (event) => handleNodeLabelPointerDown(event, node.id));
            group.appendChild(text);
            if (node.href) {
                const dimensions = nodeDimensions(node);
                const linkIndicator = svgElement('text', {
                    x: node.x + dimensions.halfWidth - 15,
                    y: node.y - dimensions.halfHeight + 20,
                    class: 'diagram-node-link-indicator',
                    'aria-hidden': 'true'
                });
                linkIndicator.textContent = '↗';
                group.appendChild(linkIndicator);
            }

            group.addEventListener('pointerdown', (event) => handleNodePointerDown(event, node.id));
            group.addEventListener('dblclick', (event) => {
                event.preventDefault();
                event.stopPropagation();
                setSingleNodeSelection(node.id);
                render();
                focusAndSelect(labelInput);
            });
            group.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    if (connectMode) handleConnectionNode(node.id);
                    else {
                        selected = { type: 'node', id: node.id };
                        selectedNodeIds = new Set([node.id]);
                        render();
                    }
                }
            });
            nodesLayer.appendChild(group);
        });
    }

    function regionMembers(region) {
        const nodesById = new Map(graph.nodes.map((node) => [node.id, node]));
        return region.nodeIds.map((id) => nodesById.get(id)).filter(Boolean);
    }

    function regionOperationSymbol(operation) {
        if (operation === 'union') return '∪';
        if (operation === 'difference') return '∖';
        return '∩';
    }

    function nodeDisplayName(node) {
        const label = String(node && node.label || '').trim();
        if (label) return label;
        const index = graph.nodes.findIndex((candidate) => candidate.id === node?.id) + 1;
        return node?.shape === 'set' ? `Adsız küme ${index || ''}`.trim() : `Şekil ${index || ''}`.trim();
    }

    function regionExpression(region) {
        const names = regionMembers(region).map(nodeDisplayName);
        if (!names.length) return 'Taralı bölge';
        if (region.operation === 'difference') {
            const removed = names.slice(1).join(' ∪ ');
            return removed ? `${names[0]} ∖ (${removed})` : names[0];
        }
        return names.join(` ${regionOperationSymbol(region.operation)} `);
    }

    function regionDisplayName(region) {
        return String(region.label || '').trim() || regionExpression(region);
    }

    function renderRegionManager(selectedRegion) {
        if (!regionManager || !regionList || !regionCount) return;
        const regions = Array.isArray(graph.regions) ? graph.regions : [];
        regionManager.hidden = regions.length === 0;
        regionCount.textContent = String(regions.length);
        regionList.replaceChildren();
        regions.forEach((region) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'diagram-region-list-item';
            button.classList.toggle('active', Boolean(selectedRegion && selectedRegion.id === region.id));
            button.setAttribute('aria-pressed', selectedRegion && selectedRegion.id === region.id ? 'true' : 'false');

            const symbol = document.createElement('span');
            symbol.className = `diagram-region-list-symbol tone-${region.tone || 'gold'}`;
            symbol.textContent = regionOperationSymbol(region.operation);
            const content = document.createElement('span');
            const name = document.createElement('strong');
            const detail = document.createElement('small');
            name.textContent = regionDisplayName(region);
            detail.textContent = `${region.nodeIds.length} şekil`;
            content.append(name, detail);
            button.append(symbol, content);
            button.addEventListener('click', () => selectRegion(region.id));
            regionList.appendChild(button);
        });
    }

    function renderRegionMemberControls(region) {
        if (
            !regionMemberList || !regionMemberCount || !regionMemberApplyButton
            || !differenceBaseField || !differenceBaseSelect
        ) return;
        regionMemberList.replaceChildren();
        differenceBaseSelect.replaceChildren();
        differenceBaseField.hidden = !region || region.operation !== 'difference';
        if (!region) {
            regionMemberDraft = null;
            regionMemberCount.textContent = '0 seçili';
            regionMemberApplyButton.disabled = true;
            return;
        }

        if (!regionMemberDraft || regionMemberDraft.regionId !== region.id) {
            regionMemberDraft = {
                regionId: region.id,
                ids: new Set(region.nodeIds),
                dirty: false
            };
        }

        const memberIds = regionMemberDraft.ids;
        const refreshDraftStatus = () => {
            const selectedCount = memberIds.size;
            const currentIds = new Set(region.nodeIds);
            const changed = selectedCount !== currentIds.size
                || Array.from(memberIds).some((id) => !currentIds.has(id));
            regionMemberDraft.dirty = changed;
            regionMemberCount.textContent = selectedCount < 2
                ? `${selectedCount} seçili · en az 2 gerekli`
                : `${selectedCount} seçili`;
            regionMemberApplyButton.disabled = selectedCount < 2 || !changed;
        };
        graph.nodes.forEach((node) => {
            const row = document.createElement('label');
            row.className = 'diagram-region-member-item';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = memberIds.has(node.id);
            row.classList.toggle('selected', checkbox.checked);
            const name = document.createElement('span');
            const type = document.createElement('small');
            name.textContent = nodeDisplayName(node);
            type.textContent = node.shape === 'set' ? 'Küme' : 'Şekil';
            row.append(checkbox, name, type);
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) memberIds.add(node.id);
                else memberIds.delete(node.id);
                row.classList.toggle('selected', checkbox.checked);
                refreshDraftStatus();
                setStatus('Bölge seçimi hazırlandı; uyguladığında diyagram güncellenecek');
            });
            regionMemberList.appendChild(row);
        });
        refreshDraftStatus();

        region.nodeIds.forEach((nodeId) => {
            const node = graph.nodes.find((item) => item.id === nodeId);
            if (!node) return;
            const option = document.createElement('option');
            option.value = node.id;
            option.textContent = nodeDisplayName(node);
            differenceBaseSelect.appendChild(option);
        });
        differenceBaseSelect.value = region.nodeIds[0] || '';
    }

    function intersectionHasVisibleArea(bounds, members) {
        const candidates = members.map((node) => ({ x: node.x, y: node.y }));
        const steps = 8;
        for (let row = 0; row <= steps; row += 1) {
            for (let column = 0; column <= steps; column += 1) {
                candidates.push({
                    x: bounds.left + ((bounds.right - bounds.left) * (column / steps)),
                    y: bounds.top + ((bounds.bottom - bounds.top) * (row / steps))
                });
            }
        }
        return candidates.some((point) => members.every((node) => pointInsideNode(point, node)));
    }

    function regionBounds(region, members) {
        if (!members.length) return null;
        const nodeBounds = members.map((node) => ({
            left: node.x - (node.width / 2),
            top: node.y - (node.height / 2),
            right: node.x + (node.width / 2),
            bottom: node.y + (node.height / 2)
        }));
        if (region.operation === 'intersection') {
            const left = Math.max(...nodeBounds.map((bounds) => bounds.left));
            const top = Math.max(...nodeBounds.map((bounds) => bounds.top));
            const right = Math.min(...nodeBounds.map((bounds) => bounds.right));
            const bottom = Math.min(...nodeBounds.map((bounds) => bounds.bottom));
            const intersection = { left, top, right, bottom };
            if (right > left && bottom > top && intersectionHasVisibleArea(intersection, members)) {
                return intersection;
            }
            return null;
        }
        if (region.operation === 'difference') return nodeBounds[0];
        return {
            left: Math.min(...nodeBounds.map((bounds) => bounds.left)),
            top: Math.min(...nodeBounds.map((bounds) => bounds.top)),
            right: Math.max(...nodeBounds.map((bounds) => bounds.right)),
            bottom: Math.max(...nodeBounds.map((bounds) => bounds.bottom))
        };
    }

    function regionLabelBasePoint(region, bounds) {
        return {
            x: (bounds.left + bounds.right) / 2,
            y: region.operation === 'intersection'
                ? (bounds.top + bounds.bottom) / 2
                : bounds.top + 24
        };
    }

    function constrainRegionLabelOffset(region, bounds, rawX, rawY) {
        const base = regionLabelBasePoint(region, bounds);
        const x = Number.isFinite(Number(rawX)) ? Number(rawX) : 0;
        const y = Number.isFinite(Number(rawY)) ? Number(rawY) : 0;
        const labelX = Math.min(WORLD_WIDTH - 12, Math.max(12, base.x + x));
        const labelY = Math.min(WORLD_HEIGHT - 12, Math.max(12, base.y + y));
        return {
            x: Math.round((labelX - base.x) * 10) / 10,
            y: Math.round((labelY - base.y) * 10) / 10
        };
    }

    function normalizeRegionLabelOffset(region, bounds) {
        const offset = constrainRegionLabelOffset(
            region,
            bounds,
            region.labelOffsetX,
            region.labelOffsetY
        );
        region.labelOffsetX = offset.x;
        region.labelOffsetY = offset.y;
        return offset;
    }

    function styleRegionShape(shape, region) {
        shape.setAttribute('fill', `url(#diagramRegionPattern-${region.tone || 'gold'})`);
        shape.setAttribute('stroke', 'none');
        shape.setAttribute('pointer-events', 'none');
    }

    function selectRegion(regionId) {
        if (!selected || selected.type !== 'region' || selected.id !== regionId) regionMemberDraft = null;
        selected = { type: 'region', id: regionId };
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('Taralı bölge seçildi');
        render();
    }

    function renderRegions() {
        regionsLayer.replaceChildren();
        regionDefs.replaceChildren();
        graph.regions.forEach((region) => {
            const members = regionMembers(region);
            if (members.length < 2) return;
            const bounds = regionBounds(region, members);
            if (!bounds) return;
            const isSelected = selected && selected.type === 'region' && selected.id === region.id;
            const group = svgElement('g', {
                class: `diagram-editor-region diagram-editor-region-${region.operation}${isSelected ? ' selected' : ''}`,
                'data-region-id': region.id
            });

            if (region.operation === 'union') {
                members.forEach((node) => {
                    const shape = renderNodeShape(node, group, 'diagram-editor-region-shape');
                    styleRegionShape(shape, region);
                });
            } else if (region.operation === 'difference') {
                const maskId = `diagram-region-mask-${region.id}`;
                const mask = svgElement('mask', {
                    id: maskId,
                    maskUnits: 'userSpaceOnUse',
                    x: 0,
                    y: 0,
                    width: WORLD_WIDTH,
                    height: WORLD_HEIGHT
                });
                mask.appendChild(svgElement('rect', { x: 0, y: 0, width: WORLD_WIDTH, height: WORLD_HEIGHT, fill: 'black' }));
                const include = renderNodeShape(members[0], mask);
                include.setAttribute('fill', 'white');
                include.setAttribute('stroke', 'none');
                members.slice(1).forEach((node) => {
                    const exclude = renderNodeShape(node, mask);
                    exclude.setAttribute('fill', 'black');
                    exclude.setAttribute('stroke', 'none');
                });
                regionDefs.appendChild(mask);
                const first = members[0];
                const visual = svgElement('rect', {
                    x: first.x - (first.width / 2),
                    y: first.y - (first.height / 2),
                    width: first.width,
                    height: first.height,
                    class: 'diagram-editor-region-shape',
                    fill: `url(#diagramRegionPattern-${region.tone || 'gold'})`,
                    mask: `url(#${maskId})`,
                    'pointer-events': 'none'
                });
                group.appendChild(visual);
            } else {
                let destination = group;
                members.slice(1).forEach((node, index) => {
                    const clipId = `diagram-region-clip-${region.id}-${index}`;
                    const clip = svgElement('clipPath', { id: clipId, clipPathUnits: 'userSpaceOnUse' });
                    renderNodeShape(node, clip);
                    regionDefs.appendChild(clip);
                    const nested = svgElement('g', { 'clip-path': `url(#${clipId})` });
                    destination.appendChild(nested);
                    destination = nested;
                });
                const shape = renderNodeShape(members[0], destination, 'diagram-editor-region-shape');
                styleRegionShape(shape, region);
            }

            const labelText = String(region.label || '').trim();
            const hitTarget = svgElement('rect', {
                x: bounds.left,
                y: bounds.top,
                width: bounds.right - bounds.left,
                height: bounds.bottom - bounds.top,
                class: 'diagram-editor-region-hit',
                tabindex: region.operation === 'intersection' ? '0' : '-1',
                role: region.operation === 'intersection' ? 'button' : 'presentation',
                'aria-label': `${labelText || 'Taralı kesişim'} bölgesini düzenle`,
                'pointer-events': region.operation === 'intersection' ? 'all' : 'none'
            });
            hitTarget.addEventListener('pointerdown', (event) => {
                event.preventDefault();
                event.stopPropagation();
                selectRegion(region.id);
            });
            hitTarget.addEventListener('keydown', (event) => {
                if (!['Enter', ' '].includes(event.key)) return;
                event.preventDefault();
                selectRegion(region.id);
            });
            group.appendChild(hitTarget);

            if (labelText) {
                const base = regionLabelBasePoint(region, bounds);
                const labelOffset = normalizeRegionLabelOffset(region, bounds);
                const labelX = base.x + labelOffset.x;
                const labelY = base.y + labelOffset.y;
                const labelGroup = svgElement('g', {
                    class: 'diagram-editor-region-label',
                    tabindex: '0',
                    role: 'button',
                    'aria-label': `${labelText} bölge adını taşımak için sürükle`
                });
                const title = svgElement('title');
                title.textContent = 'Bölge adını taşımak için sürükle';
                const label = svgElement('text', { x: labelX, y: labelY + 1 });
                label.textContent = labelText;
                labelGroup.append(title, label);
                labelGroup.addEventListener('pointerdown', (event) => {
                    handleRegionLabelPointerDown(event, region.id);
                });
                labelGroup.addEventListener('dblclick', (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    selectRegion(region.id);
                    focusAndSelect(regionLabelInput);
                });
                labelGroup.addEventListener('keydown', (event) => {
                    if (!['Enter', ' '].includes(event.key)) return;
                    event.preventDefault();
                    selectRegion(region.id);
                });
                group.appendChild(labelGroup);
            }
            regionsLayer.appendChild(group);
        });
    }

    function renderEdgeHandle() {
        handlesLayer.replaceChildren();
        const selectedConnector = getSelectedConnector();
        if (selectedConnector) {
            const connector = selectedConnector.connector;
            let geometry = null;
            let start = null;
            let end = null;
            if (selectedConnector.type === 'edge') {
                const source = graph.nodes.find((node) => node.id === connector.from);
                const target = graph.nodes.find((node) => node.id === connector.to);
                if (source && target && source.id !== target.id) {
                    const hasReverse = graph.edges.some((candidate) => (
                        candidate.from === connector.to && candidate.to === connector.from
                    ));
                    geometry = edgeGeometry(source, target, connector, hasReverse, hasReverse && connector.from > connector.to);
                    start = boundaryPoint(source, target);
                    end = boundaryPoint(target, source);
                }
            } else {
                geometry = freeArrowGeometry(connector);
                const endpoints = resolvedFreeArrowEndpoints(connector);
                start = endpoints.start;
                end = endpoints.end;
            }
            if (geometry && start && end) {
                const handle = svgElement('circle', {
                    cx: geometry.handleX,
                    cy: geometry.handleY,
                    r: 9,
                    class: 'diagram-edge-bend-handle',
                    tabindex: '0'
                });
                handle.appendChild(svgElement('title'));
                handle.firstChild.textContent = 'Oku daha fazla kıvırmak için sürükle';
                handle.addEventListener('pointerdown', (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    pushHistory();
                    if (geometry.resolvedRoute === 'straight') {
                        connector.route = 'curve';
                        connector.bend = 0;
                    }
                    edgeHandleState = {
                        type: selectedConnector.type,
                        edgeIndex: selectedConnector.index,
                        arrowId: selectedConnector.id,
                        start,
                        end,
                        route: geometry.resolvedRoute === 'straight' ? 'curve' : geometry.resolvedRoute,
                        axis: geometry.axis
                    };
                    if (canvas.setPointerCapture) canvas.setPointerCapture(event.pointerId);
                });
                handlesLayer.appendChild(handle);
            }

            if (selectedConnector.type === 'arrow') {
                const endpoints = resolvedFreeArrowEndpoints(connector);
                [['start', endpoints.start], ['end', endpoints.end]].forEach(([endpoint, point]) => {
                    const anchorProperty = endpoint === 'start' ? 'startAnchor' : 'endAnchor';
                    const anchor = connector[anchorProperty] || '';
                    const endpointHandle = svgElement('circle', {
                        cx: point.x,
                        cy: point.y,
                        r: 9,
                        class: `diagram-free-arrow-endpoint diagram-free-arrow-endpoint-${endpoint}${anchor ? ' is-anchored' : ''}${anchor && !resolveArrowAnchor(anchor) ? ' is-unavailable' : ''}`,
                        tabindex: '0'
                    });
                    endpointHandle.appendChild(svgElement('title'));
                    endpointHandle.firstChild.textContent = anchor
                        ? `${arrowAnchorLabel(anchor)} bağlantısını değiştirmek için sürükle`
                        : endpoint === 'start'
                            ? 'Okun başlangıcını taşı veya bir şeklin üzerine bırak'
                            : 'Okun ucunu taşı veya bir şeklin üzerine bırak';
                    endpointHandle.addEventListener('pointerdown', (event) => {
                        event.preventDefault();
                        event.stopPropagation();
                        pushHistory();
                        setArrowDropTarget('');
                        connector[endpoint === 'start' ? 'startX' : 'endX'] = point.x;
                        connector[endpoint === 'start' ? 'startY' : 'endY'] = point.y;
                        connector[anchorProperty] = '';
                        freeArrowEndpointState = {
                            arrowId: connector.id,
                            endpoint,
                            lastPoint: point,
                            originalAnchor: anchor,
                            moved: false
                        };
                        if (canvas.setPointerCapture) canvas.setPointerCapture(event.pointerId);
                    });
                    handlesLayer.appendChild(endpointHandle);
                });
            }
        }

        if (!selected || selected.type !== 'node' || selectedNodeIds.size !== 1) return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        const dimensions = nodeDimensions(node);
        const outline = svgElement('rect', {
            x: node.x - dimensions.halfWidth - 6,
            y: node.y - dimensions.halfHeight - 6,
            width: node.width + 12,
            height: node.height + 12,
            rx: 10,
            class: 'diagram-node-resize-outline'
        });
        const resizeHandle = svgElement('rect', {
            x: node.x + dimensions.halfWidth - 7,
            y: node.y + dimensions.halfHeight - 7,
            width: 16,
            height: 16,
            rx: 4,
            class: 'diagram-node-resize-handle',
            tabindex: '0'
        });
        resizeHandle.appendChild(svgElement('title'));
        resizeHandle.firstChild.textContent = 'Boyutlandırmak için sürükle';
        resizeHandle.addEventListener('pointerdown', (event) => {
            event.preventDefault();
            event.stopPropagation();
            pushHistory();
            nodeResizeState = {
                nodeId: node.id,
                aspectRatio: node.width / Math.max(node.height, 1),
                left: node.x - dimensions.halfWidth,
                top: node.y - dimensions.halfHeight
            };
            if (canvas.setPointerCapture) {
                try {
                    canvas.setPointerCapture(event.pointerId);
                } catch (error) {
                    // Resizing continues while the pointer stays over the canvas.
                }
            }
            setStatus('Boyutlandırmak için köşe tutamacını sürükle');
        });
        handlesLayer.append(outline, resizeHandle);
    }

    function renderInspector() {
        const selectedNode = selectedNodeIds.size === 1 && selected && selected.type === 'node'
            ? graph.nodes.find((node) => node.id === selected.id)
            : null;
        const selectedConnector = getSelectedConnector();
        const selectedEdge = selectedConnector ? selectedConnector.connector : null;
        const selectedRegion = selected && selected.type === 'region'
            ? graph.regions.find((region) => region.id === selected.id)
            : null;
        const isMultiSelection = selectedNodeIds.size > 1;
        const selectedGroup = matchingSelectedGroup();
        renderRegionManager(selectedRegion);
        renderRegionMemberControls(selectedRegion);
        labelInput.disabled = !selectedNode;
        shapeSelect.disabled = !selectedNode;
        nodeWidthInput.disabled = !selectedNode;
        nodeHeightInput.disabled = !selectedNode;
        nodeFontSizeInput.disabled = !selectedNode;
        nodeLinkInput.disabled = !selectedNode;
        nodeLinkOpenButton.disabled = !selectedNode || !normalizeNodeHref(selectedNode.href);
        labelInput.value = selectedNode ? selectedNode.label : '';
        shapeSelect.value = selectedNode ? selectedNode.shape : 'process';
        nodeWidthInput.value = selectedNode ? String(selectedNode.width) : '152';
        nodeHeightInput.value = selectedNode ? String(selectedNode.height) : '68';
        nodeWidthValue.textContent = selectedNode ? String(Math.round(selectedNode.width)) : '152';
        nodeHeightValue.textContent = selectedNode ? String(Math.round(selectedNode.height)) : '68';
        nodeFontSizeInput.value = selectedNode ? String(selectedNode.fontSize || 15) : '15';
        nodeFontSizeValue.textContent = selectedNode ? String(Math.round(selectedNode.fontSize || 15)) : '15';
        nodeLinkInput.value = selectedNode ? selectedNode.href || '' : '';
        labelInput.placeholder = selectedNode && selectedNode.shape === 'set' ? 'Küme adı (isteğe bağlı)' : 'Öğe metni';
        nodeInspector.hidden = !selectedNode;
        edgeInspector.hidden = !selectedEdge;
        if (edgeInspectorTitle) edgeInspectorTitle.textContent = selectedConnector && selectedConnector.type === 'arrow'
            ? 'Bağımsız ok'
            : 'Seçili bağlantı';
        if (edgeInspectorBadge) edgeInspectorBadge.textContent = selectedConnector && selectedConnector.type === 'arrow'
            ? 'Serbest'
            : 'Ok';
        if (arrowAnchors) {
            const selectedArrow = selectedConnector && selectedConnector.type === 'arrow'
                ? selectedConnector.connector
                : null;
            arrowAnchors.hidden = !selectedArrow;
            if (selectedArrow) {
                arrowStartAnchor.textContent = arrowAnchorLabel(selectedArrow.startAnchor);
                arrowEndAnchor.textContent = arrowAnchorLabel(selectedArrow.endAnchor);
            }
        }
        regionInspector.hidden = !selectedRegion;
        multiInspector.hidden = !isMultiSelection;
        multiSelectionCount.textContent = `${selectedNodeIds.size} düğüm`;
        groupNameField.hidden = !selectedGroup;
        groupLabelInput.value = selectedGroup ? selectedGroup.label : '';
        inspectorEmpty.hidden = Boolean(
            selectedNode || selectedEdge || selectedRegion || isMultiSelection
            || !versionsPanel.hidden || graph.regions.length
        );
        edgeLabelInput.value = selectedEdge ? selectedEdge.label || '' : '';
        edgeDescriptionInput.value = selectedEdge ? selectedEdge.description || '' : '';
        edgeStyleSelect.value = selectedEdge ? selectedEdge.style || 'solid' : 'solid';
        edgeRouteSelect.value = selectedEdge ? selectedEdge.route || 'auto' : 'auto';
        edgeBendInput.value = selectedEdge ? String(selectedEdge.bend || 0) : '0';
        edgeBendValue.textContent = selectedEdge ? String(Math.round(selectedEdge.bend || 0)) : '0';
        regionLabelInput.value = selectedRegion ? selectedRegion.label || '' : '';
        regionOperationSelect.value = selectedRegion ? selectedRegion.operation : 'intersection';
        regionToneSelect.value = selectedRegion ? selectedRegion.tone : 'gold';
        regionSymbol.textContent = selectedRegion ? regionOperationSymbol(selectedRegion.operation) : '∩';
        toneButtons.forEach((button) => {
            const active = Boolean(selectedNode && button.dataset.diagramTone === (selectedNode.tone || 'neutral'));
            button.classList.toggle('active', active);
            button.disabled = !selectedNode;
            button.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
        selectionBadge.textContent = selectedNode
            ? 'Düğüm'
            : selectedConnector && selectedConnector.type === 'arrow'
                ? 'Bağımsız ok'
                : selectedEdge ? 'Bağlantı' : selectedRegion ? 'Bölge' : isMultiSelection ? 'Çoklu' : 'Yok';
        deleteButton.disabled = !selectedEdge && !selectedRegion && selectedNodeIds.size === 0;
        copyButton.disabled = selectedNodeIds.size === 0;
        pasteButton.disabled = !clipboardGraph || graph.nodes.length >= MAX_NODES;
        duplicateButton.disabled = selectedNodeIds.size === 0 || graph.nodes.length >= MAX_NODES;
        alignHorizontalButton.disabled = selectedNodeIds.size < 2;
        alignVerticalButton.disabled = selectedNodeIds.size < 2;
        distributeButton.disabled = selectedNodeIds.size < 3;
        groupButton.disabled = selectedNodeIds.size < 2 || graph.groups.length >= MAX_GROUPS;
        ungroupButton.disabled = !graph.groups.some((group) => group.nodeIds.some((id) => selectedNodeIds.has(id)));
        regionMenuButton.disabled = selectedNodeIds.size < 2 || graph.regions.length >= MAX_REGIONS;
        undoButton.disabled = history.length === 0;
        redoButton.disabled = redoHistory.length === 0;
        nodeCount.textContent = graph.nodes.length;
        edgeCount.textContent = graph.edges.length + (graph.arrows || []).length;
        if (freeArrowButton) freeArrowButton.disabled = (graph.arrows || []).length >= MAX_FREE_ARROWS;
        connectButton.classList.toggle('active', connectMode);
        connectButton.setAttribute('aria-pressed', connectMode ? 'true' : 'false');
        snapButton.classList.toggle('active', snapEnabled);
        snapButton.setAttribute('aria-pressed', snapEnabled ? 'true' : 'false');
        versionsButton.classList.toggle('active', !versionsPanel.hidden);
        versionsButton.setAttribute('aria-pressed', versionsPanel.hidden ? 'false' : 'true');
        applyViewport();
    }

    function render() {
        renderGroups();
        renderEdges();
        renderNodes();
        renderRegions();
        renderEdgeHandle();
        renderInspector();
        renderMiniMap();
    }

    function handleRegionLabelPointerDown(event, regionId) {
        event.preventDefault();
        event.stopPropagation();
        if (pinchState) return;
        if (spacePanActive || event.button === 1) {
            startPan(event, false);
            return;
        }
        const region = graph.regions.find((item) => item.id === regionId);
        if (!region) return;
        const members = regionMembers(region);
        const bounds = regionBounds(region, members);
        if (!bounds) return;
        if (!selected || selected.type !== 'region' || selected.id !== regionId) regionMemberDraft = null;
        selected = { type: 'region', id: regionId };
        selectedNodeIds.clear();
        disableConnectMode(false);
        const offset = normalizeRegionLabelOffset(region, bounds);
        const point = canvasPoint(event);
        regionLabelDragState = {
            regionId,
            startPoint: point,
            startOffsetX: offset.x,
            startOffsetY: offset.y,
            startClientX: event.clientX,
            startClientY: event.clientY,
            moved: false,
            historyPushed: false
        };
        if (canvas.setPointerCapture) {
            try {
                canvas.setPointerCapture(event.pointerId);
            } catch (error) {
                // Pointer capture is an enhancement; dragging still works inside the canvas.
            }
        }
        setStatus('Bölge adını taşımak için sürükle');
        render();
    }

    function handleNodeLabelPointerDown(event, nodeId) {
        event.preventDefault();
        event.stopPropagation();
        if (pinchState) return;
        if (spacePanActive || event.button === 1) {
            startPan(event, false);
            return;
        }
        if (connectMode) {
            handleConnectionNode(nodeId);
            return;
        }
        if (event.shiftKey || event.ctrlKey || event.metaKey) {
            toggleNodeSelection(nodeId);
            setStatus(`${selectedNodeIds.size} düğüm seçildi`);
            render();
            return;
        }
        const node = graph.nodes.find((item) => item.id === nodeId);
        if (!node) return;
        setSingleNodeSelection(nodeId);
        const point = canvasPoint(event);
        labelDragState = {
            nodeId,
            startPoint: point,
            startOffsetX: Number(node.labelOffsetX) || 0,
            startOffsetY: Number(node.labelOffsetY) || 0,
            startClientX: event.clientX,
            startClientY: event.clientY,
            moved: false,
            historyPushed: false
        };
        if (canvas.setPointerCapture) {
            try {
                canvas.setPointerCapture(event.pointerId);
            } catch (error) {
                // Pointer capture is an enhancement; dragging still works inside the canvas.
            }
        }
        setStatus('Yazıyı şeklin içinde taşımak için sürükle');
        render();
    }

    function handleNodePointerDown(event, nodeId) {
        event.stopPropagation();
        if (pinchState) return;
        if (spacePanActive || event.button === 1) {
            startPan(event, false);
            return;
        }
        if (connectMode) {
            handleConnectionNode(nodeId);
            return;
        }

        const node = graph.nodes.find((item) => item.id === nodeId);
        if (!node) return;
        if (event.shiftKey || event.ctrlKey || event.metaKey) {
            event.preventDefault();
            toggleNodeSelection(nodeId);
            setStatus(`${selectedNodeIds.size} düğüm seçildi`);
            render();
            return;
        }
        if (!selectedNodeIds.has(nodeId)) setSingleNodeSelection(nodeId);
        else if (selectedNodeIds.size === 1) selected = { type: 'node', id: nodeId };
        const point = canvasPoint(event);
        dragState = {
            nodeIds: Array.from(selectedNodeIds),
            startPoint: point,
            startPositions: new Map(selectedNodes().map((item) => [item.id, { x: item.x, y: item.y }])),
            startClientX: event.clientX,
            startClientY: event.clientY,
            moved: false,
            historyPushed: false
        };
        if (canvas.setPointerCapture) {
            try {
                canvas.setPointerCapture(event.pointerId);
            } catch (error) {
                // Pointer capture is an enhancement; dragging still works inside the canvas.
            }
        }
        render();
        if (event.detail > 1 && selectedNodeIds.size === 1) focusAndSelect(labelInput);
    }

    function startPan(event, startedOnBackground = false) {
        event.preventDefault();
        const point = rootCanvasPoint(event);
        panState = {
            startPoint: point,
            panX: viewState.panX,
            panY: viewState.panY,
            startClientX: event.clientX,
            startClientY: event.clientY,
            startedOnBackground,
            moved: false
        };
        if (canvas.setPointerCapture) {
            try {
                canvas.setPointerCapture(event.pointerId);
            } catch (error) {
                // The drag continues while the pointer remains over the canvas.
            }
        }
        canvas.classList.add('is-panning');
    }

    function handleConnectionNode(nodeId) {
        setSingleNodeSelection(nodeId);
        if (!connectSource) {
            connectSource = nodeId;
            setStatus('Bağlantının biteceği düğümü seç');
            render();
            return;
        }

        const duplicate = graph.edges.some((edge) => edge.from === connectSource && edge.to === nodeId);
        if (!duplicate && graph.edges.length < MAX_EDGES) {
            pushHistory();
            graph.edges.push({
                from: connectSource,
                to: nodeId,
                label: '',
                style: 'solid',
                description: '',
                route: 'auto',
                bend: 0
            });
            setStatus(connectSource === nodeId ? 'Düğüm içi döngü eklendi' : 'Bağlantı eklendi');
        } else if (duplicate) {
            setStatus('Bu bağlantı zaten var');
        }
        disableConnectMode(false);
        render();
    }

    function disableConnectMode(updateStatus = true) {
        connectMode = false;
        connectSource = null;
        if (updateStatus) setStatus('Bir düğüm veya bağlantı seç');
    }

    function addNode(shape) {
        if (graph.nodes.length >= MAX_NODES) {
            setStatus(`En fazla ${MAX_NODES} düğüm eklenebilir`);
            return;
        }
        pushHistory();
        const offset = graph.nodes.length * 34;
        const labels = {
            decision: 'Karar',
            terminal: 'Başlangıç / bitiş',
            data: 'Veri',
            document: 'Belge',
            pyramid: 'Piramit katmanı',
            set: '',
            label: 'Bölge etiketi',
            process: 'Yeni adım'
        };
        const dimensions = {
            decision: { width: 180, height: 104 },
            pyramid: { width: 280, height: 92 },
            set: { width: 280, height: 220 },
            label: { width: 180, height: 52 }
        }[shape] || { width: 180, height: 76 };
        const viewportCenterX = ((VIEWPORT_WIDTH / 2) - viewState.panX) / viewState.zoom;
        const viewportCenterY = ((VIEWPORT_HEIGHT / 2) - viewState.panY) / viewState.zoom;
        const node = {
            id: takeNextNodeId(),
            label: labels[shape] || 'Yeni adım',
            shape,
            tone: 'neutral',
            x: Math.min(WORLD_WIDTH - (dimensions.width / 2) - 8, Math.max((dimensions.width / 2) + 8, viewportCenterX + (offset % 180))),
            y: Math.min(WORLD_HEIGHT - (dimensions.height / 2) - 8, Math.max((dimensions.height / 2) + 8, viewportCenterY + (offset % 140))),
            width: dimensions.width,
            height: dimensions.height,
            href: '',
            fontSize: shape === 'label' ? 17 : 15,
            labelOffsetX: 0,
            labelOffsetY: 0
        };
        graph.nodes.push(node);
        setSingleNodeSelection(node.id);
        disableConnectMode(false);
        setStatus('Yeni düğüm eklendi');
        render();
        labelInput.focus();
        labelInput.select();
    }

    function addFreeArrow() {
        if ((graph.arrows || []).length >= MAX_FREE_ARROWS) {
            setStatus(`En fazla ${MAX_FREE_ARROWS} bağımsız ok eklenebilir`);
            return;
        }
        pushHistory();
        const centerX = ((VIEWPORT_WIDTH / 2) - viewState.panX) / viewState.zoom;
        const centerY = ((VIEWPORT_HEIGHT / 2) - viewState.panY) / viewState.zoom;
        const id = `a${Date.now().toString(36)}${(graph.arrows || []).length}`;
        const arrow = {
            id,
            startX: Math.min(WORLD_WIDTH - 8, Math.max(8, centerX - 150)),
            startY: Math.min(WORLD_HEIGHT - 8, Math.max(8, centerY)),
            endX: Math.min(WORLD_WIDTH - 8, Math.max(8, centerX + 150)),
            endY: Math.min(WORLD_HEIGHT - 8, Math.max(8, centerY)),
            label: '',
            style: 'solid',
            description: '',
            route: 'straight',
            bend: 0,
            startAnchor: '',
            endAnchor: ''
        };
        if (!Array.isArray(graph.arrows)) graph.arrows = [];
        graph.arrows.push(arrow);
        selected = { type: 'arrow', id };
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('Bağımsız ok eklendi; uçlarını sürükleyebilirsin');
        render();
    }

    function createRegion(operation) {
        const memberIds = Array.from(selectedNodeIds);
        if (memberIds.length < 2 || graph.regions.length >= MAX_REGIONS) return;
        const members = memberIds
            .map((id) => graph.nodes.find((node) => node.id === id))
            .filter(Boolean);
        if (members.length < 2) return;
        pushHistory();
        const region = {
            id: `r${Date.now().toString(36)}${graph.regions.length}`,
            label: '',
            operation,
            tone: operation === 'intersection' ? 'gold' : operation === 'union' ? 'blue' : 'green',
            nodeIds: memberIds
        };
        graph.regions.push(region);
        selectedNodeIds.clear();
        selected = { type: 'region', id: region.id };
        setStatus(`${regionOperationSymbol(operation)} bölgesi oluşturuldu`);
        render();
    }

    function copySelection() {
        const nodes = selectedNodes();
        if (!nodes.length) return false;
        const nodeIds = new Set(nodes.map((node) => node.id));
        clipboardGraph = {
            nodes: cloneGraph(nodes),
            edges: cloneGraph(graph.edges.filter((edge) => nodeIds.has(edge.from) && nodeIds.has(edge.to))),
            groups: cloneGraph(graph.groups.filter((group) => group.nodeIds.every((id) => nodeIds.has(id)))),
            regions: cloneGraph(graph.regions.filter((region) => region.nodeIds.every((id) => nodeIds.has(id))))
        };
        setStatus(`${nodes.length} düğüm kopyalandı`);
        renderInspector();
        return true;
    }

    function pasteSelection() {
        if (!clipboardGraph || !clipboardGraph.nodes.length) return false;
        const available = MAX_NODES - graph.nodes.length;
        if (available <= 0) {
            setStatus('Düğüm sınırına ulaşıldı');
            return false;
        }
        const nodesToPaste = clipboardGraph.nodes.slice(0, available);
        pushHistory();
        const idMap = new Map();
        const pasted = nodesToPaste.map((source) => {
            const id = takeNextNodeId();
            idMap.set(source.id, id);
            const width = Number(source.width) || 152;
            const height = Number(source.height) || 68;
            return {
                ...cloneGraph(source),
                id,
                x: Math.min(WORLD_WIDTH - (width / 2) - 8, Math.max((width / 2) + 8, source.x + 42)),
                y: Math.min(WORLD_HEIGHT - (height / 2) - 8, Math.max((height / 2) + 8, source.y + 42))
            };
        });
        graph.nodes.push(...pasted);
        clipboardGraph.edges.forEach((edge) => {
            if (graph.edges.length >= MAX_EDGES || !idMap.has(edge.from) || !idMap.has(edge.to)) return;
            graph.edges.push({ ...cloneGraph(edge), from: idMap.get(edge.from), to: idMap.get(edge.to) });
        });
        clipboardGraph.groups.forEach((group) => {
            if (graph.groups.length >= MAX_GROUPS) return;
            const memberIds = group.nodeIds.map((id) => idMap.get(id)).filter(Boolean);
            if (memberIds.length < 2) return;
            graph.groups.push({
                ...cloneGraph(group),
                id: `g${Date.now().toString(36)}${graph.groups.length}`,
                nodeIds: memberIds
            });
        });
        (clipboardGraph.regions || []).forEach((region) => {
            if (graph.regions.length >= MAX_REGIONS) return;
            const memberIds = region.nodeIds.map((id) => idMap.get(id)).filter(Boolean);
            if (memberIds.length < 2) return;
            graph.regions.push({
                ...cloneGraph(region),
                id: `r${Date.now().toString(36)}${graph.regions.length}`,
                nodeIds: memberIds
            });
        });
        selectedNodeIds = new Set(pasted.map((node) => node.id));
        selected = pasted.length === 1 ? { type: 'node', id: pasted[0].id } : null;
        setStatus(`${pasted.length} düğüm yapıştırıldı`);
        render();
        return true;
    }

    function duplicateSelectedNode() {
        if (!copySelection()) return;
        if (pasteSelection()) setStatus('Seçim çoğaltıldı');
    }

    function alignSelection(axis) {
        const nodes = selectedNodes();
        if (nodes.length < 2) return;
        pushHistory();
        const value = nodes.reduce((sum, node) => sum + node[axis], 0) / nodes.length;
        nodes.forEach((node) => {
            node[axis] = snapEnabled ? Math.round(value / 24) * 24 : value;
        });
        setStatus(axis === 'y' ? 'Düğümler yatay hizalandı' : 'Düğümler dikey hizalandı');
        render();
    }

    function distributeSelection() {
        const nodes = selectedNodes();
        if (nodes.length < 3) return;
        pushHistory();
        const xSpread = Math.max(...nodes.map((node) => node.x)) - Math.min(...nodes.map((node) => node.x));
        const ySpread = Math.max(...nodes.map((node) => node.y)) - Math.min(...nodes.map((node) => node.y));
        const axis = xSpread >= ySpread ? 'x' : 'y';
        nodes.sort((a, b) => a[axis] - b[axis]);
        const start = nodes[0][axis];
        const end = nodes[nodes.length - 1][axis];
        const step = (end - start) / (nodes.length - 1);
        nodes.forEach((node, index) => {
            node[axis] = start + (step * index);
        });
        setStatus('Düğümler eşit aralıkla dağıtıldı');
        render();
    }

    function groupSelection() {
        if (selectedNodeIds.size < 2 || graph.groups.length >= MAX_GROUPS) return;
        pushHistory();
        graph.groups = graph.groups.flatMap((group) => {
            const nodeIds = group.nodeIds.filter((id) => !selectedNodeIds.has(id));
            return nodeIds.length >= 2 ? [{ ...group, nodeIds }] : [];
        });
        const group = {
            id: `g${Date.now().toString(36)}`,
            label: `Grup ${graph.groups.length + 1}`,
            tone: 'neutral',
            nodeIds: Array.from(selectedNodeIds)
        };
        graph.groups.push(group);
        setStatus('Seçili düğümler gruplandı');
        render();
        window.requestAnimationFrame(() => groupLabelInput.focus());
    }

    function ungroupSelection() {
        const before = graph.groups.length;
        const remaining = graph.groups.filter((group) => !group.nodeIds.some((id) => selectedNodeIds.has(id)));
        if (remaining.length === before) return;
        pushHistory();
        graph.groups = remaining;
        setStatus('Grup çözüldü');
        render();
    }

    function arrangeGraph() {
        if (!graph.nodes.length) return;
        pushHistory();
        const nodeIds = new Set(graph.nodes.map((node) => node.id));
        const incoming = new Map(graph.nodes.map((node) => [node.id, 0]));
        const outgoing = new Map(graph.nodes.map((node) => [node.id, []]));
        graph.edges.forEach((edge) => {
            if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to) || edge.from === edge.to) return;
            incoming.set(edge.to, (incoming.get(edge.to) || 0) + 1);
            outgoing.get(edge.from).push(edge.to);
        });

        const roots = graph.nodes.filter((node) => incoming.get(node.id) === 0).map((node) => node.id);
        const queue = roots.length ? [...roots] : [graph.nodes[0].id];
        const levels = new Map(queue.map((id) => [id, 0]));
        while (queue.length) {
            const nodeId = queue.shift();
            const nextLevel = (levels.get(nodeId) || 0) + 1;
            (outgoing.get(nodeId) || []).forEach((targetId) => {
                if (levels.has(targetId)) return;
                levels.set(targetId, nextLevel);
                queue.push(targetId);
            });
        }

        let fallbackLevel = Math.max(0, ...levels.values());
        graph.nodes.forEach((node) => {
            if (!levels.has(node.id)) levels.set(node.id, ++fallbackLevel);
        });
        const groups = new Map();
        graph.nodes.forEach((node) => {
            const level = levels.get(node.id);
            if (!groups.has(level)) groups.set(level, []);
            groups.get(level).push(node);
        });
        const orderedLevels = Array.from(groups.keys()).sort((a, b) => a - b);
        const xStep = 300;
        orderedLevels.forEach((level, levelIndex) => {
            const nodes = groups.get(level);
            const yStep = 150;
            nodes.forEach((node, nodeIndex) => {
                node.x = orderedLevels.length > 1 ? 180 + (levelIndex * xStep) : VIEWPORT_WIDTH / 2;
                node.y = 120 + (nodeIndex * yStep);
            });
        });
        selected = null;
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('Düğümler akış yönüne göre düzenlendi');
        render();
        fitGraph();
    }

    function deleteSelected() {
        if (!selected && selectedNodeIds.size === 0) return;
        pushHistory();
        if (selected && selected.type === 'edge') {
            graph.edges.splice(selected.index, 1);
            setStatus('Bağlantı silindi');
        } else if (selected && selected.type === 'arrow') {
            graph.arrows = (graph.arrows || []).filter((arrow) => arrow.id !== selected.id);
            setStatus('Bağımsız ok silindi');
        } else if (selected && selected.type === 'region') {
            const removedAnchor = `r:${selected.id}`;
            graph.regions = graph.regions.filter((region) => region.id !== selected.id);
            (graph.arrows || []).forEach((arrow) => {
                if (arrow.startAnchor === removedAnchor) arrow.startAnchor = '';
                if (arrow.endAnchor === removedAnchor) arrow.endAnchor = '';
            });
            setStatus('Taralı bölge silindi');
        } else {
            const removedIds = new Set(selectedNodeIds);
            const previousRegionIds = new Set(graph.regions.map((region) => region.id));
            graph.nodes = graph.nodes.filter((node) => !removedIds.has(node.id));
            graph.edges = graph.edges.filter((edge) => !removedIds.has(edge.from) && !removedIds.has(edge.to));
            graph.groups = graph.groups.flatMap((group) => {
                const nodeIds = group.nodeIds.filter((id) => !removedIds.has(id));
                return nodeIds.length >= 2 ? [{ ...group, nodeIds }] : [];
            });
            graph.regions = graph.regions.flatMap((region) => {
                const nodeIds = region.nodeIds.filter((id) => !removedIds.has(id));
                return nodeIds.length >= 2 ? [{ ...region, nodeIds }] : [];
            });
            const remainingRegionIds = new Set(graph.regions.map((region) => region.id));
            (graph.arrows || []).forEach((arrow) => {
                ['startAnchor', 'endAnchor'].forEach((property) => {
                    const anchor = arrow[property] || '';
                    if (anchor.startsWith('n:') && removedIds.has(anchor.slice(2))) arrow[property] = '';
                    if (anchor.startsWith('r:') && previousRegionIds.has(anchor.slice(2)) && !remainingRegionIds.has(anchor.slice(2))) {
                        arrow[property] = '';
                    }
                });
            });
            setStatus(`${removedIds.size} düğüm ve bağlantıları silindi`);
        }
        selected = null;
        selectedNodeIds.clear();
        disableConnectMode(false);
        render();
    }

    function utf8Base64Url(value) {
        const bytes = new TextEncoder().encode(value);
        let binary = '';
        const chunkSize = 8192;
        for (let index = 0; index < bytes.length; index += chunkSize) {
            binary += String.fromCharCode(...bytes.subarray(index, index + chunkSize));
        }
        return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
    }

    function insertAtSelection(textarea, marker) {
        const start = textarea.selectionStart || 0;
        const end = textarea.selectionEnd || start;
        const before = textarea.value.slice(0, start);
        const after = textarea.value.slice(end);
        const prefix = before && !before.endsWith('\n\n') ? (before.endsWith('\n') ? '\n' : '\n\n') : '';
        const suffix = after && !after.startsWith('\n\n') ? (after.startsWith('\n') ? '\n' : '\n\n') : '';
        const insertion = `${prefix}${marker}${suffix}`;
        textarea.value = `${before}${insertion}${after}`;
        const caret = before.length + insertion.length;
        textarea.setSelectionRange(caret, caret);
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        textarea.dispatchEvent(new Event('change', { bubbles: true }));
        textarea.focus();
    }

    function replaceDiagramMarker(textarea, marker) {
        if (!editingMarker) {
            insertAtSelection(textarea, marker);
            return;
        }
        let start = editingMarker.start;
        let end = editingMarker.end;
        if (textarea.value.slice(start, end) !== editingMarker.marker) {
            start = textarea.value.indexOf(editingMarker.marker);
            if (start < 0) {
                insertAtSelection(textarea, marker);
                return;
            }
            end = start + editingMarker.marker.length;
        }
        textarea.value = `${textarea.value.slice(0, start)}${marker}${textarea.value.slice(end)}`;
        const caret = start + marker.length;
        textarea.setSelectionRange(caret, caret);
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
        textarea.dispatchEvent(new Event('change', { bubbles: true }));
        textarea.focus();
    }

    function showFeedback(message, type) {
        if (typeof window.showToast === 'function') {
            window.showToast(message, type || 'success');
            return;
        }
        setStatus(message);
    }

    function openEditor(textarea, encodedHint) {
        activeTextarea = textarea;
        const marker = findDiagramMarker(textarea, encodedHint);
        if (!marker) {
            editingMarker = null;
            selectTemplate('cycle');
            editorTitle.textContent = 'Akışı oluştur';
            insertButton.innerHTML = '<i class="bi bi-plus-lg" aria-hidden="true"></i> Metne ekle';
        } else {
            loadGraph(marker.graph, marker);
        }
        const instance = bootstrap.Modal.getOrCreateInstance(editorModal);
        instance.show();
    }

    function injectToolbarButtons() {
        const textareas = Array.from(document.querySelectorAll('textarea[name="answer_text"], textarea[id$="answer_text"]'));
        const seen = new Set();
        textareas.forEach((textarea) => {
            if (seen.has(textarea) || textarea.dataset.diagramEnabled === '1') return;
            seen.add(textarea);
            textarea.dataset.diagramEnabled = '1';
            const form = textarea.closest('form');
            if (!form) return;

            let toolbar = form.querySelector('.btn-toolbar');
            if (!toolbar) {
                toolbar = document.createElement('div');
                toolbar.className = 'btn-toolbar mb-2';
                toolbar.setAttribute('role', 'toolbar');
                textarea.parentNode.insertBefore(toolbar, textarea);
            }

            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'btn btn-sm btn-outline-theme-secondary me-2 diagram-entry-button';
            button.title = 'Diyagram ekle';
            button.innerHTML = '<i class="bi bi-diagram-3" aria-hidden="true"></i> Diyagram';
            button.addEventListener('click', () => openEditor(textarea));

            const imageButton = toolbar.querySelector('.insert-image-btn');
            if (imageButton) imageButton.insertAdjacentElement('afterend', button);
            else toolbar.appendChild(button);
        });
    }

    document.querySelectorAll('[data-diagram-template]').forEach((button) => {
        button.addEventListener('click', () => selectTemplate(button.dataset.diagramTemplate));
    });

    document.querySelectorAll('[data-diagram-add]').forEach((button) => {
        button.addEventListener('click', () => {
            addNode(button.dataset.diagramAdd);
            const menu = button.closest('.dropdown');
            const trigger = menu && menu.querySelector('[data-bs-toggle="dropdown"]');
            if (trigger && window.bootstrap && bootstrap.Dropdown) {
                bootstrap.Dropdown.getOrCreateInstance(trigger).hide();
            }
        });
    });

    document.querySelectorAll('[data-diagram-region]').forEach((button) => {
        button.addEventListener('click', () => {
            createRegion(button.dataset.diagramRegion);
            const menu = button.closest('.dropdown');
            const trigger = menu && menu.querySelector('[data-bs-toggle="dropdown"]');
            if (trigger && window.bootstrap && bootstrap.Dropdown) {
                bootstrap.Dropdown.getOrCreateInstance(trigger).hide();
            }
        });
    });

    connectButton.addEventListener('click', () => {
        connectMode = !connectMode;
        connectSource = null;
        selected = null;
        selectedNodeIds.clear();
        setStatus(connectMode ? 'Bağlantının başlayacağı düğümü seç' : 'Bağlantı modu kapatıldı');
        render();
    });
    if (freeArrowButton) freeArrowButton.addEventListener('click', addFreeArrow);

    duplicateButton.addEventListener('click', duplicateSelectedNode);
    copyButton.addEventListener('click', copySelection);
    pasteButton.addEventListener('click', pasteSelection);
    alignHorizontalButton.addEventListener('click', () => alignSelection('y'));
    alignVerticalButton.addEventListener('click', () => alignSelection('x'));
    distributeButton.addEventListener('click', distributeSelection);
    groupButton.addEventListener('click', groupSelection);
    ungroupButton.addEventListener('click', ungroupSelection);
    arrangeButton.addEventListener('click', arrangeGraph);
    snapButton.addEventListener('click', () => {
        snapEnabled = !snapEnabled;
        setStatus(snapEnabled ? 'Izgaraya hizalama açık' : 'Serbest yerleştirme açık');
        renderInspector();
    });

    if (inspectorToggleButton && editorLayout) {
        inspectorToggleButton.addEventListener('click', () => {
            const collapsed = editorLayout.classList.toggle('inspector-collapsed');
            inspectorToggleButton.classList.toggle('active', collapsed);
            inspectorToggleButton.setAttribute('aria-pressed', collapsed ? 'true' : 'false');
            inspectorToggleButton.setAttribute('aria-label', collapsed ? 'Ayar panelini göster' : 'Ayar panelini gizle');
            window.setTimeout(() => canvas.focus({ preventScroll: true }), 180);
        });
    }
    zoomOutButton.addEventListener('click', () => zoomAt(viewState.zoom / 1.2));
    zoomInButton.addEventListener('click', () => zoomAt(viewState.zoom * 1.2));
    fitButton.addEventListener('click', fitGraph);
    versionsButton.addEventListener('click', () => {
        versionsPanel.hidden = !versionsPanel.hidden;
        if (!versionsPanel.hidden) renderVersionList();
        renderInspector();
    });
    versionsCloseButton.addEventListener('click', () => {
        versionsPanel.hidden = true;
        renderInspector();
    });
    saveVersionButton.addEventListener('click', () => {
        saveLocalVersion('Elle kaydedilen sürüm');
        renderVersionList();
        setStatus('Şimdiki sürüm kaydedildi');
    });

    undoButton.addEventListener('click', () => {
        if (!history.length) return;
        redoHistory.push(JSON.stringify(graph));
        graph = normalizeGraphForEditor(JSON.parse(history.pop()));
        syncNextNodeNumber();
        titleInput.value = graph.title;
        selected = null;
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('Son işlem geri alındı');
        render();
    });

    redoButton.addEventListener('click', () => {
        if (!redoHistory.length) return;
        history.push(JSON.stringify(graph));
        graph = normalizeGraphForEditor(JSON.parse(redoHistory.pop()));
        syncNextNodeNumber();
        titleInput.value = graph.title;
        selected = null;
        selectedNodeIds.clear();
        disableConnectMode(false);
        setStatus('İşlem yeniden uygulandı');
        render();
    });

    deleteButton.addEventListener('click', deleteSelected);

    titleInput.addEventListener('input', () => {
        graph.title = titleInput.value.slice(0, 80);
    });

    labelInput.addEventListener('focus', () => {
        if (selected && selected.type === 'node') pushHistory();
    });

    labelInput.addEventListener('input', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        node.label = labelInput.value.slice(0, 240);
        normalizeNodeLabelOffset(node);
        renderEdges();
        renderNodes();
        renderRegions();
        renderMiniMap();
    });
    labelInput.addEventListener('blur', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        const fallback = defaultNodeLabel(node.shape);
        node.label = node.label.trim().slice(0, 240) || fallback;
        labelInput.value = node.label;
        render();
    });

    shapeSelect.addEventListener('change', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        pushHistory();
        node.shape = shapeSelect.value;
        if (node.shape === 'decision' && node.height < 92) node.height = 104;
        if (node.shape === 'pyramid') {
            node.width = Math.max(node.width, 280);
            node.height = Math.max(node.height, 92);
        }
        if (node.shape === 'set') {
            node.width = Math.max(node.width, 280);
            node.height = Math.max(node.height, 220);
        }
        if (node.shape === 'label') {
            node.width = Math.max(node.width, 160);
            node.height = Math.max(MIN_NODE_HEIGHT, Math.min(node.height, 72));
        }
        normalizeNodeLabelOffset(node);
        render();
    });

    function updateNodeSize(property, input, output) {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        const limits = property === 'width'
            ? [MIN_NODE_WIDTH, MAX_NODE_WIDTH]
            : [MIN_NODE_HEIGHT, MAX_NODE_HEIGHT];
        node[property] = Math.min(limits[1], Math.max(limits[0], Number(input.value) || limits[0]));
        normalizeNodeLabelOffset(node);
        output.textContent = String(Math.round(node[property]));
        const dimensions = nodeDimensions(node);
        node.x = Math.min(WORLD_WIDTH - dimensions.halfWidth - 8, Math.max(dimensions.halfWidth + 8, node.x));
        node.y = Math.min(WORLD_HEIGHT - dimensions.halfHeight - 8, Math.max(dimensions.halfHeight + 8, node.y));
        renderGroups();
        renderEdges();
        renderNodes();
        renderRegions();
        renderMiniMap();
    }

    [nodeWidthInput, nodeHeightInput, nodeFontSizeInput].forEach((input) => {
        input.addEventListener('pointerdown', () => {
            if (selected && selected.type === 'node') pushHistory();
        });
    });
    nodeWidthInput.addEventListener('input', () => updateNodeSize('width', nodeWidthInput, nodeWidthValue));
    nodeHeightInput.addEventListener('input', () => updateNodeSize('height', nodeHeightInput, nodeHeightValue));
    nodeFontSizeInput.addEventListener('input', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        node.fontSize = Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, Number(nodeFontSizeInput.value) || 15));
        normalizeNodeLabelOffset(node);
        nodeFontSizeValue.textContent = String(Math.round(node.fontSize));
        renderNodes();
        renderRegions();
    });

    nodeLinkInput.addEventListener('focus', () => {
        if (selected && selected.type === 'node') pushHistory();
    });
    nodeLinkInput.addEventListener('input', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (node) {
            node.href = nodeLinkInput.value.slice(0, 500);
            nodeLinkOpenButton.disabled = !normalizeNodeHref(node.href);
        }
    });
    nodeLinkInput.addEventListener('blur', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        const rawValue = node.href;
        node.href = normalizeNodeHref(rawValue);
        nodeLinkInput.value = node.href;
        nodeLinkOpenButton.disabled = !node.href;
        if (!node.href && rawValue.trim()) setStatus('Yalnızca http(s) veya site içi bağlantı kullanılabilir');
    });
    nodeLinkOpenButton.addEventListener('click', () => {
        if (!selected || selected.type !== 'node') return;
        const node = graph.nodes.find((item) => item.id === selected.id);
        if (!node) return;
        const href = normalizeNodeHref(nodeLinkInput.value || node.href);
        if (!href) {
            setStatus('Önce geçerli bir bağlantı yaz');
            return;
        }
        node.href = href;
        nodeLinkInput.value = href;
        if (openDiagramHref(href)) setStatus('Bağlantı yeni sekmede açıldı');
    });

    toneButtons.forEach((button) => {
        button.addEventListener('click', () => {
            if (!selected || selected.type !== 'node') return;
            const node = graph.nodes.find((item) => item.id === selected.id);
            if (!node || node.tone === button.dataset.diagramTone) return;
            pushHistory();
            node.tone = button.dataset.diagramTone;
            render();
        });
    });

    edgeLabelInput.addEventListener('focus', () => {
        if (getSelectedConnector()) pushHistory();
    });

    edgeLabelInput.addEventListener('input', () => {
        const edge = getSelectedConnector()?.connector;
        if (!edge) return;
        edge.label = edgeLabelInput.value.slice(0, 50);
        renderEdges();
        renderEdgeHandle();
    });

    edgeDescriptionInput.addEventListener('focus', () => {
        if (getSelectedConnector()) pushHistory();
    });
    edgeDescriptionInput.addEventListener('input', () => {
        const edge = getSelectedConnector()?.connector;
        if (edge) edge.description = edgeDescriptionInput.value.slice(0, 600);
    });

    edgeStyleSelect.addEventListener('change', () => {
        const edge = getSelectedConnector()?.connector;
        if (!edge) return;
        pushHistory();
        edge.style = edgeStyleSelect.value === 'dashed' ? 'dashed' : 'solid';
        render();
    });

    edgeRouteSelect.addEventListener('change', () => {
        const edge = getSelectedConnector()?.connector;
        if (!edge) return;
        pushHistory();
        edge.route = ['auto', 'straight', 'curve', 'orthogonal'].includes(edgeRouteSelect.value)
            ? edgeRouteSelect.value
            : 'auto';
        if (edge.route === 'straight' || edge.route === 'auto') edge.bend = 0;
        setStatus('Ok rotası güncellendi');
        render();
    });

    edgeBendInput.addEventListener('pointerdown', () => {
        if (getSelectedConnector()) pushHistory();
    });
    edgeBendInput.addEventListener('input', () => {
        const edge = getSelectedConnector()?.connector;
        if (!edge) return;
        edge.bend = Math.min(MAX_EDGE_BEND, Math.max(-MAX_EDGE_BEND, Number(edgeBendInput.value) || 0));
        if (edge.route === 'straight' || edge.route === 'auto') edge.route = 'curve';
        edgeRouteSelect.value = edge.route;
        edgeBendValue.textContent = String(Math.round(edge.bend));
        renderEdges();
        renderEdgeHandle();
    });

    groupLabelInput.addEventListener('focus', () => {
        if (matchingSelectedGroup()) pushHistory();
    });
    groupLabelInput.addEventListener('input', () => {
        const group = matchingSelectedGroup();
        if (!group) return;
        group.label = groupLabelInput.value.slice(0, 80) || 'Grup';
        renderGroups();
    });

    regionLabelInput.addEventListener('focus', () => {
        if (selected && selected.type === 'region') pushHistory();
    });
    regionLabelInput.addEventListener('input', () => {
        if (!selected || selected.type !== 'region') return;
        const region = graph.regions.find((item) => item.id === selected.id);
        if (!region) return;
        region.label = regionLabelInput.value.slice(0, 80);
        renderRegions();
        renderRegionManager(region);
    });
    regionOperationSelect.addEventListener('change', () => {
        if (!selected || selected.type !== 'region') return;
        const region = graph.regions.find((item) => item.id === selected.id);
        if (!region) return;
        pushHistory();
        region.operation = ['intersection', 'union', 'difference'].includes(regionOperationSelect.value)
            ? regionOperationSelect.value
            : 'intersection';
        regionSymbol.textContent = regionOperationSymbol(region.operation);
        setStatus('Bölge işlemi güncellendi');
        render();
    });
    differenceBaseSelect.addEventListener('change', () => {
        if (!selected || selected.type !== 'region') return;
        const region = graph.regions.find((item) => item.id === selected.id);
        const baseId = differenceBaseSelect.value;
        if (!region || region.operation !== 'difference' || !region.nodeIds.includes(baseId) || region.nodeIds[0] === baseId) return;
        pushHistory();
        region.nodeIds = [baseId, ...region.nodeIds.filter((id) => id !== baseId)];
        setStatus(`Farkın korunan tarafı ${nodeDisplayName(graph.nodes.find((node) => node.id === baseId))} olarak değiştirildi`);
        render();
    });
    regionMemberApplyButton.addEventListener('click', () => {
        if (!selected || selected.type !== 'region' || !regionMemberDraft) return;
        const region = graph.regions.find((item) => item.id === selected.id);
        if (!region || region.id !== regionMemberDraft.regionId || regionMemberDraft.ids.size < 2) return;
        const nextIds = [
            ...region.nodeIds.filter((id) => regionMemberDraft.ids.has(id)),
            ...graph.nodes
                .map((node) => node.id)
                .filter((id) => regionMemberDraft.ids.has(id) && !region.nodeIds.includes(id))
        ];
        const unchanged = nextIds.length === region.nodeIds.length
            && nextIds.every((id, index) => id === region.nodeIds[index]);
        if (unchanged) return;
        pushHistory();
        region.nodeIds = nextIds;
        regionMemberDraft = null;
        setStatus('Bölgenin şekilleri güncellendi');
        render();
    });
    regionToneSelect.addEventListener('change', () => {
        if (!selected || selected.type !== 'region') return;
        const region = graph.regions.find((item) => item.id === selected.id);
        if (!region) return;
        pushHistory();
        region.tone = ['neutral', 'green', 'blue', 'gold', 'red'].includes(regionToneSelect.value)
            ? regionToneSelect.value
            : 'gold';
        render();
    });

    canvas.addEventListener('pointermove', (event) => {
        if (event.pointerType === 'touch' && activeTouchPointers.has(event.pointerId)) {
            activeTouchPointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
        }
        if (pinchState && activeTouchPointers.size >= 2) {
            const points = Array.from(activeTouchPointers.values()).slice(0, 2);
            const distance = Math.max(1, Math.hypot(points[1].x - points[0].x, points[1].y - points[0].y));
            const centerEvent = {
                clientX: (points[0].x + points[1].x) / 2,
                clientY: (points[0].y + points[1].y) / 2
            };
            const center = rootCanvasPoint(centerEvent);
            const zoom = clampZoom(pinchState.zoom * (distance / pinchState.distance));
            viewState.zoom = zoom;
            viewState.panX = center.x - (pinchState.contentX * zoom);
            viewState.panY = center.y - (pinchState.contentY * zoom);
            applyViewport();
            return;
        }
        if (panState) {
            const point = rootCanvasPoint(event);
            if (!panState.moved && Math.hypot(
                event.clientX - panState.startClientX,
                event.clientY - panState.startClientY
            ) >= 3) panState.moved = true;
            viewState.panX = panState.panX + (point.x - panState.startPoint.x);
            viewState.panY = panState.panY + (point.y - panState.startPoint.y);
            applyViewport();
            return;
        }

        if (regionLabelDragState) {
            const region = graph.regions.find((item) => item.id === regionLabelDragState.regionId);
            if (!region) return;
            const members = regionMembers(region);
            const bounds = regionBounds(region, members);
            if (!bounds) return;
            if (!regionLabelDragState.moved) {
                const distance = Math.hypot(
                    event.clientX - regionLabelDragState.startClientX,
                    event.clientY - regionLabelDragState.startClientY
                );
                if (distance < 4) return;
                regionLabelDragState.moved = true;
                if (!regionLabelDragState.historyPushed) {
                    pushHistory();
                    regionLabelDragState.historyPushed = true;
                }
            }
            const point = canvasPoint(event);
            const offset = constrainRegionLabelOffset(
                region,
                bounds,
                regionLabelDragState.startOffsetX + point.x - regionLabelDragState.startPoint.x,
                regionLabelDragState.startOffsetY + point.y - regionLabelDragState.startPoint.y
            );
            region.labelOffsetX = offset.x;
            region.labelOffsetY = offset.y;
            renderRegions();
            return;
        }

        if (labelDragState) {
            const node = graph.nodes.find((item) => item.id === labelDragState.nodeId);
            if (!node) return;
            if (!labelDragState.moved) {
                const distance = Math.hypot(
                    event.clientX - labelDragState.startClientX,
                    event.clientY - labelDragState.startClientY
                );
                if (distance < 4) return;
                labelDragState.moved = true;
                if (!labelDragState.historyPushed) {
                    pushHistory();
                    labelDragState.historyPushed = true;
                }
            }
            const point = canvasPoint(event);
            const offset = constrainNodeLabelOffset(
                node,
                labelDragState.startOffsetX + point.x - labelDragState.startPoint.x,
                labelDragState.startOffsetY + point.y - labelDragState.startPoint.y
            );
            node.labelOffsetX = offset.x;
            node.labelOffsetY = offset.y;
            renderNodes();
            return;
        }

        if (nodeResizeState) {
            const node = graph.nodes.find((item) => item.id === nodeResizeState.nodeId);
            if (!node) return;
            const point = canvasPoint(event);
            const maximumWidth = Math.min(MAX_NODE_WIDTH, WORLD_WIDTH - nodeResizeState.left - 8);
            const maximumHeight = Math.min(MAX_NODE_HEIGHT, WORLD_HEIGHT - nodeResizeState.top - 8);
            let width = Math.min(maximumWidth, Math.max(MIN_NODE_WIDTH, point.x - nodeResizeState.left));
            let height = Math.min(maximumHeight, Math.max(MIN_NODE_HEIGHT, point.y - nodeResizeState.top));
            if (event.shiftKey) {
                const ratio = nodeResizeState.aspectRatio || 1;
                if (width / Math.max(height, 1) > ratio) height = Math.min(maximumHeight, width / ratio);
                else width = Math.min(maximumWidth, height * ratio);
            }
            node.width = snapEnabled ? Math.round(width / 8) * 8 : width;
            node.height = snapEnabled ? Math.round(height / 8) * 8 : height;
            node.x = nodeResizeState.left + (node.width / 2);
            node.y = nodeResizeState.top + (node.height / 2);
            normalizeNodeLabelOffset(node);
            nodeWidthInput.value = String(Math.round(node.width));
            nodeHeightInput.value = String(Math.round(node.height));
            nodeWidthValue.textContent = String(Math.round(node.width));
            nodeHeightValue.textContent = String(Math.round(node.height));
            renderGroups();
            renderEdges();
            renderNodes();
            renderRegions();
            renderEdgeHandle();
            renderMiniMap();
            return;
        }

        if (freeArrowEndpointState) {
            const arrow = (graph.arrows || []).find((item) => item.id === freeArrowEndpointState.arrowId);
            if (!arrow) return;
            const point = canvasPoint(event);
            const x = snapEnabled ? Math.round(point.x / 8) * 8 : point.x;
            const y = snapEnabled ? Math.round(point.y / 8) * 8 : point.y;
            const clampedPoint = {
                x: Math.min(WORLD_WIDTH - 8, Math.max(8, x)),
                y: Math.min(WORLD_HEIGHT - 8, Math.max(8, y))
            };
            arrow[freeArrowEndpointState.endpoint === 'start' ? 'startX' : 'endX'] = clampedPoint.x;
            arrow[freeArrowEndpointState.endpoint === 'start' ? 'startY' : 'endY'] = clampedPoint.y;
            freeArrowEndpointState.lastPoint = clampedPoint;
            freeArrowEndpointState.moved = true;
            setArrowDropTarget(findArrowAnchorAtPoint(clampedPoint));
            renderEdges();
            renderEdgeHandle();
            renderMiniMap();
            return;
        }

        if (edgeHandleState) {
            const edge = edgeHandleState.type === 'arrow'
                ? (graph.arrows || []).find((arrow) => arrow.id === edgeHandleState.arrowId)
                : graph.edges[edgeHandleState.edgeIndex];
            if (!edge) return;
            const point = canvasPoint(event);
            const start = edgeHandleState.start;
            const end = edgeHandleState.end;
            if (edgeHandleState.route === 'orthogonal') {
                if (edgeHandleState.axis === 'x') {
                    edge.bend = point.x - ((start.x + end.x) / 2);
                } else {
                    edge.bend = point.y - ((start.y + end.y) / 2);
                }
            } else {
                const dx = end.x - start.x;
                const dy = end.y - start.y;
                const length = Math.max(Math.hypot(dx, dy), 1);
                const midpointX = (start.x + end.x) / 2;
                const midpointY = (start.y + end.y) / 2;
                edge.bend = 2 * (
                    ((point.x - midpointX) * (-dy / length))
                    + ((point.y - midpointY) * (dx / length))
                );
            }
            edge.bend = Math.round(Math.min(MAX_EDGE_BEND, Math.max(-MAX_EDGE_BEND, edge.bend)));
            edgeBendInput.value = String(edge.bend);
            edgeBendValue.textContent = String(edge.bend);
            edgeRouteSelect.value = edge.route;
            renderEdges();
            renderEdgeHandle();
            return;
        }

        if (!dragState) return;
        if (!dragState.moved) {
            const distance = Math.hypot(
                event.clientX - dragState.startClientX,
                event.clientY - dragState.startClientY
            );
            if (distance < 4) return;
            dragState.moved = true;
            if (!dragState.historyPushed) {
                pushHistory();
                dragState.historyPushed = true;
            }
        }
        const point = canvasPoint(event);
        const deltaX = point.x - dragState.startPoint.x;
        const deltaY = point.y - dragState.startPoint.y;
        dragState.nodeIds.forEach((nodeId) => {
            const node = graph.nodes.find((item) => item.id === nodeId);
            const startPosition = dragState.startPositions.get(nodeId);
            if (!node || !startPosition) return;
            const dimensions = nodeDimensions(node);
            const rawX = startPosition.x + deltaX;
            const rawY = startPosition.y + deltaY;
            const nextX = snapEnabled ? Math.round(rawX / 24) * 24 : rawX;
            const nextY = snapEnabled ? Math.round(rawY / 24) * 24 : rawY;
            node.x = Math.min(WORLD_WIDTH - dimensions.halfWidth - 8, Math.max(dimensions.halfWidth + 8, nextX));
            node.y = Math.min(WORLD_HEIGHT - dimensions.halfHeight - 8, Math.max(dimensions.halfHeight + 8, nextY));
        });
        renderGroups();
        renderEdges();
        renderNodes();
        renderRegions();
        renderEdgeHandle();
        renderMiniMap();
    });

    function endPointerInteraction() {
        if (panState) {
            const { moved, startedOnBackground } = panState;
            panState = null;
            canvas.classList.remove('is-panning');
            if (!moved && startedOnBackground) {
                selected = null;
                selectedNodeIds.clear();
                disableConnectMode(false);
                render();
                setStatus('Seçim temizlendi');
            } else if (moved) {
                setStatus('Tuval taşındı');
            }
        }
        if (edgeHandleState) {
            edgeHandleState = null;
            setStatus('Ok bükümü güncellendi');
            render();
        }
        if (freeArrowEndpointState) {
            const arrow = (graph.arrows || []).find((item) => item.id === freeArrowEndpointState.arrowId);
            const endpoint = freeArrowEndpointState.endpoint;
            const anchor = freeArrowEndpointState.moved
                ? freeArrowDropAnchor || findArrowAnchorAtPoint(freeArrowEndpointState.lastPoint || { x: 0, y: 0 })
                : freeArrowEndpointState.originalAnchor;
            if (arrow) arrow[endpoint === 'start' ? 'startAnchor' : 'endAnchor'] = anchor;
            freeArrowEndpointState = null;
            setArrowDropTarget('');
            setStatus(anchor ? `Ok ucu ${arrowAnchorLabel(anchor)} öğesine bağlandı` : 'Bağımsız okun ucu serbest bırakıldı');
            render();
        }
        if (nodeResizeState) {
            nodeResizeState = null;
            setStatus('Öğe boyutu güncellendi');
            render();
        }
        if (regionLabelDragState) {
            const moved = regionLabelDragState.moved;
            regionLabelDragState = null;
            setStatus(moved ? 'Bölge adı taşındı' : 'Taralı bölge seçildi');
            renderInspector();
        }
        if (labelDragState) {
            const moved = labelDragState.moved;
            labelDragState = null;
            setStatus(moved ? 'Şekil içindeki yazı taşındı' : 'Düğüm seçildi');
            renderInspector();
        }
        if (dragState) {
            const moved = dragState.moved;
            dragState = null;
            setStatus(moved ? 'Düğümler taşındı' : 'Düğüm seçildi');
            renderInspector();
        }
    }

    canvas.addEventListener('pointerup', endPointerInteraction);
    canvas.addEventListener('pointercancel', endPointerInteraction);
    canvas.addEventListener('pointerdown', (event) => {
        if (event.pointerType !== 'touch') return;
        activeTouchPointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
        if (activeTouchPointers.size < 2) return;
        const points = Array.from(activeTouchPointers.values()).slice(0, 2);
        const center = rootCanvasPoint({
            clientX: (points[0].x + points[1].x) / 2,
            clientY: (points[0].y + points[1].y) / 2
        });
        pinchState = {
            distance: Math.max(1, Math.hypot(points[1].x - points[0].x, points[1].y - points[0].y)),
            zoom: viewState.zoom,
            contentX: (center.x - viewState.panX) / viewState.zoom,
            contentY: (center.y - viewState.panY) / viewState.zoom
        };
        dragState = null;
        labelDragState = null;
        regionLabelDragState = null;
        panState = null;
        edgeHandleState = null;
        freeArrowEndpointState = null;
        setArrowDropTarget('');
        nodeResizeState = null;
        canvas.classList.add('is-panning');
    }, true);
    const releaseTouchPointer = (event) => {
        if (event.pointerType !== 'touch') return;
        const wasPinching = Boolean(pinchState);
        activeTouchPointers.delete(event.pointerId);
        if (activeTouchPointers.size < 2) pinchState = null;
        if (wasPinching) {
            canvas.classList.remove('is-panning');
            setStatus('Görünüm güncellendi');
        }
    };
    canvas.addEventListener('pointerup', releaseTouchPointer, true);
    canvas.addEventListener('pointercancel', releaseTouchPointer, true);
    canvas.addEventListener('pointerdown', (event) => {
        if (pinchState) return;
        const background = event.target === canvas || event.target.classList.contains('diagram-grid-background');
        if (background || event.button === 1 || spacePanActive) {
            startPan(event, background);
            return;
        }
    });

    canvas.addEventListener('wheel', (event) => {
        event.preventDefault();
        const anchor = rootCanvasPoint(event);
        zoomAt(viewState.zoom * (event.deltaY > 0 ? 0.9 : 1.1), anchor);
    }, { passive: false });

    miniMap.addEventListener('pointerdown', (event) => {
        const point = miniMap.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        const matrix = miniMap.getScreenCTM();
        const mapped = matrix ? point.matrixTransform(matrix.inverse()) : { x: VIEWPORT_WIDTH / 2, y: VIEWPORT_HEIGHT / 2 };
        viewState.panX = (VIEWPORT_WIDTH / 2) - (mapped.x * viewState.zoom);
        viewState.panY = (VIEWPORT_HEIGHT / 2) - (mapped.y * viewState.zoom);
        applyViewport();
        setStatus('Mini haritadan konum değiştirildi');
    });

    insertButton.addEventListener('click', () => {
        if (!activeTextarea) return;
        graph.title = titleInput.value.trim().slice(0, 80) || 'Diyagram';
        graph.nodes.forEach((node) => {
            const fallback = defaultNodeLabel(node.shape);
            node.label = String(node.label ?? fallback).trim().slice(0, 240) || fallback;
            node.tone = node.tone || 'neutral';
            node.x = Math.round(node.x * 10) / 10;
            node.y = Math.round(node.y * 10) / 10;
            node.width = Math.min(MAX_NODE_WIDTH, Math.max(MIN_NODE_WIDTH, Number(node.width) || 152));
            node.height = Math.min(MAX_NODE_HEIGHT, Math.max(MIN_NODE_HEIGHT, Number(node.height) || 68));
            node.href = normalizeNodeHref(node.href);
            node.fontSize = Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, Number(node.fontSize) || 15));
        });
        graph.edges.forEach((edge) => {
            edge.label = String(edge.label || '').trim().slice(0, 50);
            edge.style = edge.style === 'dashed' ? 'dashed' : 'solid';
            edge.description = String(edge.description || '').trim().slice(0, 600);
            edge.route = ['auto', 'straight', 'curve', 'orthogonal'].includes(edge.route) ? edge.route : 'auto';
            edge.bend = Math.min(MAX_EDGE_BEND, Math.max(-MAX_EDGE_BEND, Number(edge.bend) || 0));
        });
        (graph.arrows || []).forEach((arrow) => {
            arrow.startX = Math.round(Math.min(WORLD_WIDTH - 8, Math.max(8, Number(arrow.startX) || 8)) * 10) / 10;
            arrow.startY = Math.round(Math.min(WORLD_HEIGHT - 8, Math.max(8, Number(arrow.startY) || 8)) * 10) / 10;
            arrow.endX = Math.round(Math.min(WORLD_WIDTH - 8, Math.max(8, Number(arrow.endX) || 8)) * 10) / 10;
            arrow.endY = Math.round(Math.min(WORLD_HEIGHT - 8, Math.max(8, Number(arrow.endY) || 8)) * 10) / 10;
            arrow.label = String(arrow.label || '').trim().slice(0, 50);
            arrow.style = arrow.style === 'dashed' ? 'dashed' : 'solid';
            arrow.description = String(arrow.description || '').trim().slice(0, 600);
            arrow.route = ['auto', 'straight', 'curve', 'orthogonal'].includes(arrow.route) ? arrow.route : 'straight';
            arrow.bend = Math.min(MAX_EDGE_BEND, Math.max(-MAX_EDGE_BEND, Number(arrow.bend) || 0));
        });
        if (graph.nodes.length < 1 && !(graph.arrows || []).length) {
            setStatus('Metne eklemek için en az bir öğe veya bağımsız ok gerekli');
            return;
        }
        const payload = normalizeGraphForEditor(graph);
        graph = payload;
        syncNextNodeNumber();
        const marker = `[[diyagram:${utf8Base64Url(JSON.stringify(packGraph(payload)))}]]`;
        const wasEditing = Boolean(editingMarker);
        bootstrap.Modal.getInstance(editorModal).hide();
        replaceDiagramMarker(activeTextarea, marker);
        showFeedback(wasEditing ? 'Diyagram güncellendi.' : 'Diyagram metne eklendi.', 'success');
    });

    function findEditableTextareaForPayload(encodedPayload) {
        const textareas = Array.from(document.querySelectorAll('textarea[name="answer_text"], textarea[id$="answer_text"]'));
        return textareas.find((textarea) => textarea.value.includes(`[[diyagram:${encodedPayload}]]`)) || null;
    }

    function hideViewerInfo() {
        viewerInfo.hidden = true;
        viewerInfoTitle.textContent = 'Bağlantı';
        viewerInfoText.textContent = '';
        viewerStage.classList.remove('has-info');
        viewerInfo.style.removeProperty('--diagram-info-left');
        viewerInfo.style.removeProperty('--diagram-info-top');
    }

    function showViewerInfo(title, description, anchor) {
        viewerInfoTitle.textContent = title || 'Bağlantı';
        viewerInfoText.textContent = description || '';
        viewerInfo.hidden = false;
        viewerStage.classList.add('has-info');
        if (!anchor) return;
        window.requestAnimationFrame(() => {
            const modalContent = viewerModal.querySelector('.diagram-viewer-modal');
            if (!modalContent) return;
            const modalRect = modalContent.getBoundingClientRect();
            const anchorRect = anchor.getBoundingClientRect();
            const infoWidth = Math.min(360, Math.max(280, viewerInfo.offsetWidth || 320));
            const infoHeight = viewerInfo.offsetHeight || 140;
            let left = anchorRect.right - modalRect.left + 14;
            let top = anchorRect.top - modalRect.top + ((anchorRect.height - infoHeight) / 2);
            if (left + infoWidth > modalRect.width - 16) {
                left = anchorRect.left - modalRect.left - infoWidth - 14;
                viewerInfo.classList.add('opens-left');
            } else {
                viewerInfo.classList.remove('opens-left');
            }
            left = Math.max(16, Math.min(left, modalRect.width - infoWidth - 16));
            top = Math.max(78, Math.min(top, modalRect.height - infoHeight - 76));
            viewerInfo.style.setProperty('--diagram-info-left', `${left}px`);
            viewerInfo.style.setProperty('--diagram-info-top', `${top}px`);
        });
    }

    function activateViewerInteractions(svg) {
        svg.querySelectorAll('.answer-diagram-edge-interactive').forEach((edgeGroup) => {
            const openDescription = (event) => {
                event.preventDefault();
                event.stopPropagation();
                showViewerInfo(
                    edgeGroup.dataset.diagramEdgeLabel || 'Bağlantı',
                    edgeGroup.dataset.diagramEdgeDescription || '',
                    edgeGroup
                );
            };
            edgeGroup.addEventListener('click', openDescription);
            edgeGroup.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') openDescription(event);
            });
        });
        svg.querySelectorAll('.answer-diagram-node-linked').forEach((node) => {
            const openLink = (event) => {
                event.preventDefault();
                event.stopPropagation();
                openDiagramHref(node.dataset.diagramLink);
            };
            node.addEventListener('click', openLink);
            node.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') openLink(event);
            });
        });
    }

    function findDiagramEditUrl(figure) {
        let scope = figure;
        for (let depth = 0; scope && scope !== document.body && depth < 7; depth += 1) {
            const editLink = Array.from(scope.querySelectorAll('a[href*="/answer/"]')).find((link) => (
                /\/answer\/\d+\/edit\/(?:\?|#|$)/.test(link.getAttribute('href') || '')
            ));
            if (editLink) return editLink.href;
            if (scope.matches('.answer, .answer-card, [id^="answer-"]')) return '';
            scope = scope.parentElement;
        }
        return '';
    }

    function diagramPositionInAnswer(figure) {
        const scope = figure.closest('.answer-text') || figure.closest('.answer') || document;
        return Math.max(0, Array.from(scope.querySelectorAll('.answer-diagram')).indexOf(figure));
    }

    function directDiagramEditUrl(figure, editUrl) {
        if (!editUrl) return '';
        const url = new URL(editUrl, window.location.href);
        const diagramId = figure && figure.dataset.diagramId;
        if (diagramId) url.searchParams.set('edit_diagram', diagramId);
        if (figure) url.searchParams.set('diagram_position', String(diagramPositionInAnswer(figure)));
        return url.href;
    }

    function openDiagramViewer(figure, requestedEdgeIndex) {
        const sourceSvg = figure && figure.querySelector('svg');
        if (!figure || !sourceSvg) return;
        viewerTitle.textContent = figure.dataset.diagramTitle || 'Diyagram';
        const encodedPayload = figure.dataset.diagramPayload || '';
        const editableTextarea = findEditableTextareaForPayload(encodedPayload);
        const editUrl = findDiagramEditUrl(figure);
        viewerContext = {
            encodedPayload,
            editableTextarea,
            editUrl,
            figure,
            sourceSvg
        };
        hideViewerInfo();
        editDiagramButton.hidden = !editableTextarea && !editUrl;
        const clone = sourceSvg.cloneNode(true);
        const marker = clone.querySelector('marker[id]');
        if (marker) {
            const markerId = `${marker.id}-viewer-${Date.now()}`;
            marker.id = markerId;
            clone.querySelectorAll('[marker-end]').forEach((path) => {
                path.setAttribute('marker-end', `url(#${markerId})`);
            });
        }
        viewerStage.replaceChildren(clone);
        activateViewerInteractions(clone);
        if (requestedEdgeIndex !== null) {
            viewerModal.addEventListener('shown.bs.modal', () => {
                const edge = clone.querySelector(`[data-diagram-edge-index="${requestedEdgeIndex}"]`);
                if (edge) showViewerInfo(
                    edge.dataset.diagramEdgeLabel || 'Bağlantı',
                    edge.dataset.diagramEdgeDescription || '',
                    edge
                );
            }, { once: true });
        }
        bootstrap.Modal.getOrCreateInstance(viewerModal).show();
    }

    function diagramCollapseKey(figure) {
        const id = figure.dataset.diagramId || figure.dataset.diagramPayload?.slice(0, 32) || 'diagram';
        return `hafif-diagram-collapsed:${id}`;
    }

    function setDiagramCollapsed(figure, collapsed) {
        const toggle = figure.querySelector('.answer-diagram-toggle');
        figure.classList.toggle('is-collapsed', collapsed);
        if (toggle) {
            toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
            toggle.setAttribute('aria-label', `${figure.dataset.diagramTitle || 'Diyagram'} diyagramını ${collapsed ? 'göster' : 'gizle'}`);
            toggle.title = collapsed ? 'Diyagramı göster' : 'Diyagramı gizle';
            const icon = toggle.querySelector('i');
            if (icon) icon.className = `bi ${collapsed ? 'bi-chevron-down' : 'bi-chevron-up'}`;
        }
        try {
            localStorage.setItem(diagramCollapseKey(figure), collapsed ? '1' : '0');
        } catch (error) {
            // Storage errors do not block the local open/close state.
        }
    }

    function restoreDiagramCollapseState(root) {
        (root || document).querySelectorAll('.answer-diagram').forEach((figure) => {
            try {
                if (localStorage.getItem(diagramCollapseKey(figure)) === '1') {
                    setDiagramCollapsed(figure, true);
                }
            } catch (error) {
                // Ignore unavailable storage.
            }
        });
    }

    function decoratePublishedDiagrams(root) {
        (root || document).querySelectorAll('.answer-diagram').forEach((figure) => {
            const actions = figure.querySelector('.answer-diagram-actions');
            const editUrl = findDiagramEditUrl(figure);
            if (!actions || !editUrl || actions.querySelector('.answer-diagram-edit')) return;
            const editButton = document.createElement('button');
            editButton.type = 'button';
            editButton.className = 'answer-diagram-edit';
            editButton.dataset.editUrl = editUrl;
            editButton.dataset.diagramId = figure.dataset.diagramId || '';
            editButton.dataset.diagramPosition = String(diagramPositionInAnswer(figure));
            editButton.title = 'Diyagramı düzenle';
            editButton.setAttribute('aria-label', `${figure.dataset.diagramTitle || 'Diyagram'} diyagramını düzenle`);
            editButton.innerHTML = '<i class="bi bi-pencil" aria-hidden="true"></i><span>Düzenle</span>';
            actions.prepend(editButton);
        });
    }

    document.addEventListener('click', (event) => {
        const editControl = event.target.closest('.answer-diagram-edit');
        if (editControl) {
            event.preventDefault();
            const editUrl = editControl.dataset.editUrl;
            const figure = editControl.closest('.answer-diagram');
            const destination = directDiagramEditUrl(figure, editUrl);
            if (destination) window.location.href = destination;
            return;
        }

        const toggle = event.target.closest('.answer-diagram-toggle');
        if (toggle) {
            event.preventDefault();
            const figure = toggle.closest('.answer-diagram');
            if (figure) setDiagramCollapsed(figure, !figure.classList.contains('is-collapsed'));
            return;
        }

        const linkedNode = event.target.closest('.answer-diagram-node-linked');
        if (linkedNode && !linkedNode.closest('#diagramViewerStage')) {
            event.preventDefault();
            event.stopPropagation();
            openDiagramHref(linkedNode.dataset.diagramLink);
            return;
        }

        const requestedEdge = event.target.closest('.answer-diagram-edge-interactive');
        const trigger = event.target.closest('.answer-diagram-open, .answer-diagram-expand, .answer-diagram-body');
        if (!trigger && !requestedEdge) return;
        const figure = (requestedEdge || trigger).closest('.answer-diagram');
        if (!figure) return;
        event.preventDefault();
        openDiagramViewer(figure, requestedEdge ? requestedEdge.dataset.diagramEdgeIndex : null);
    });

    document.addEventListener('keydown', (event) => {
        const linkedNode = event.target.closest('.answer-diagram-node-linked');
        if (!linkedNode || linkedNode.closest('#diagramViewerStage')) return;
        if (event.key !== 'Enter' && event.key !== ' ') return;
        event.preventDefault();
        event.stopPropagation();
        openDiagramHref(linkedNode.dataset.diagramLink);
    });

    viewerInfoClose.addEventListener('click', hideViewerInfo);
    viewerStage.addEventListener('click', (event) => {
        if (!event.target.closest('.answer-diagram-edge-interactive')) hideViewerInfo();
    });

    editDiagramButton.addEventListener('click', () => {
        if (!viewerContext) return;
        const { editableTextarea, encodedPayload, editUrl, figure } = viewerContext;
        if (!editableTextarea && editUrl) {
            window.location.href = directDiagramEditUrl(figure, editUrl);
            return;
        }
        if (!editableTextarea) return;
        viewerModal.addEventListener('hidden.bs.modal', () => {
            openEditor(editableTextarea, encodedPayload);
        }, { once: true });
        bootstrap.Modal.getInstance(viewerModal).hide();
    });

    decoratePublishedDiagrams();
    restoreDiagramCollapseState();

    function diagramFileName() {
        return (viewerTitle.textContent || 'diyagram')
            .normalize('NFKD')
            .replace(/[^\w\s-]/g, '')
            .trim()
            .replace(/\s+/g, '-')
            .toLowerCase() || 'diyagram';
    }

    function prepareExportSvg() {
        const sourceSvg = viewerStage.querySelector('svg');
        if (!sourceSvg) return null;
        const clone = sourceSvg.cloneNode(true);
        const viewBox = (sourceSvg.getAttribute('viewBox') || `0 0 ${VIEWPORT_WIDTH} ${VIEWPORT_HEIGHT}`)
            .trim().split(/\s+/).map(Number);
        const exportBounds = {
            x: Number.isFinite(viewBox[0]) ? viewBox[0] : 0,
            y: Number.isFinite(viewBox[1]) ? viewBox[1] : 0,
            width: Number.isFinite(viewBox[2]) && viewBox[2] > 0 ? viewBox[2] : VIEWPORT_WIDTH,
            height: Number.isFinite(viewBox[3]) && viewBox[3] > 0 ? viewBox[3] : VIEWPORT_HEIGHT
        };
        clone.setAttribute('xmlns', SVG_NS);
        clone.setAttribute('width', String(exportBounds.width));
        clone.setAttribute('height', String(exportBounds.height));
        clone.dataset.exportWidth = String(exportBounds.width);
        clone.dataset.exportHeight = String(exportBounds.height);
        const sourceElements = [sourceSvg, ...sourceSvg.querySelectorAll('*')];
        const clonedElements = [clone, ...clone.querySelectorAll('*')];
        sourceElements.forEach((element, index) => {
            const target = clonedElements[index];
            if (!target) return;
            const computed = window.getComputedStyle(element);
            const properties = ['fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'font-family', 'font-size', 'font-weight', 'text-anchor', 'paint-order'];
            const inlineStyle = properties
                .map((property) => `${property}:${computed.getPropertyValue(property)}`)
                .join(';');
            target.setAttribute('style', inlineStyle);
        });
        clone.querySelectorAll('.answer-diagram-edge-hit').forEach((element) => element.remove());
        clone.querySelectorAll('[tabindex]').forEach((element) => element.removeAttribute('tabindex'));
        const background = svgElement('rect', {
            x: exportBounds.x,
            y: exportBounds.y,
            width: exportBounds.width,
            height: exportBounds.height,
            fill: window.getComputedStyle(sourceSvg).backgroundColor || '#ffffff'
        });
        const defs = clone.querySelector('defs');
        if (defs && defs.nextSibling) clone.insertBefore(background, defs.nextSibling);
        else clone.insertBefore(background, clone.firstChild);
        return clone;
    }

    function downloadBlob(blob, extension) {
        const url = URL.createObjectURL(blob);
        const download = document.createElement('a');
        download.href = url;
        download.download = `${diagramFileName()}.${extension}`;
        document.body.appendChild(download);
        download.click();
        download.remove();
        window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    async function exportCanvas(scale) {
        const svg = prepareExportSvg();
        if (!svg) return null;
        const content = new XMLSerializer().serializeToString(svg);
        const blob = new Blob([content], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        try {
            const image = new Image();
            await new Promise((resolve, reject) => {
                image.onload = resolve;
                image.onerror = reject;
                image.src = url;
            });
            const output = document.createElement('canvas');
            const sourceWidth = Number(svg.dataset.exportWidth) || VIEWPORT_WIDTH;
            const sourceHeight = Number(svg.dataset.exportHeight) || VIEWPORT_HEIGHT;
            const baseWidth = Math.min(1600, Math.max(VIEWPORT_WIDTH, sourceWidth));
            const baseHeight = baseWidth * (sourceHeight / sourceWidth);
            output.width = Math.round(baseWidth * scale);
            output.height = Math.round(baseHeight * scale);
            const context = output.getContext('2d');
            context.fillStyle = '#ffffff';
            context.fillRect(0, 0, output.width, output.height);
            context.drawImage(image, 0, 0, output.width, output.height);
            return output;
        } finally {
            URL.revokeObjectURL(url);
        }
    }

    function canvasBlob(canvas, type, quality) {
        return new Promise((resolve, reject) => {
            canvas.toBlob((blob) => {
                if (blob) resolve(blob);
                else reject(new Error('Canvas output failed'));
            }, type, quality);
        });
    }

    function concatBytes(parts) {
        const total = parts.reduce((sum, part) => sum + part.length, 0);
        const output = new Uint8Array(total);
        let offset = 0;
        parts.forEach((part) => {
            output.set(part, offset);
            offset += part.length;
        });
        return output;
    }

    function buildPdf(jpegBytes, imageWidth, imageHeight) {
        const encoder = new TextEncoder();
        const parts = [];
        const offsets = [0];
        let length = 0;
        const add = (part) => {
            const bytes = typeof part === 'string' ? encoder.encode(part) : part;
            parts.push(bytes);
            length += bytes.length;
        };
        const addObject = (number, body) => {
            offsets[number] = length;
            add(`${number} 0 obj\n${body}\nendobj\n`);
        };

        add('%PDF-1.4\n%diagram\n');
        addObject(1, '<< /Type /Catalog /Pages 2 0 R >>');
        addObject(2, '<< /Type /Pages /Kids [3 0 R] /Count 1 >>');
        const pageWidth = 720;
        const pageHeight = Math.max(240, Math.min(720, pageWidth * (imageHeight / imageWidth)));
        addObject(3, `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageWidth} ${pageHeight.toFixed(2)}] /Resources << /XObject << /Im0 4 0 R >> >> /Contents 5 0 R >>`);
        offsets[4] = length;
        add(`4 0 obj\n<< /Type /XObject /Subtype /Image /Width ${imageWidth} /Height ${imageHeight} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${jpegBytes.length} >>\nstream\n`);
        add(jpegBytes);
        add('\nendstream\nendobj\n');
        const stream = `q ${pageWidth} 0 0 ${pageHeight.toFixed(2)} 0 0 cm /Im0 Do Q`;
        addObject(5, `<< /Length ${stream.length} >>\nstream\n${stream}\nendstream`);
        const xrefOffset = length;
        add('xref\n0 6\n0000000000 65535 f \n');
        for (let index = 1; index <= 5; index += 1) {
            add(`${String(offsets[index]).padStart(10, '0')} 00000 n \n`);
        }
        add(`trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`);
        return new Blob([concatBytes(parts)], { type: 'application/pdf' });
    }

    downloadDiagramButton.addEventListener('click', () => {
        const svg = prepareExportSvg();
        if (!svg) return;
        const content = new XMLSerializer().serializeToString(svg);
        downloadBlob(new Blob([content], { type: 'image/svg+xml;charset=utf-8' }), 'svg');
    });

    downloadDiagramPngButton.addEventListener('click', async () => {
        try {
            const output = await exportCanvas(2);
            if (!output) return;
            downloadBlob(await canvasBlob(output, 'image/png'), 'png');
        } catch (error) {
            showFeedback('PNG oluşturulamadı.', 'error');
        }
    });

    downloadDiagramPdfButton.addEventListener('click', async () => {
        try {
            const output = await exportCanvas(2);
            if (!output) return;
            const jpeg = await canvasBlob(output, 'image/jpeg', 0.94);
            const jpegBytes = new Uint8Array(await jpeg.arrayBuffer());
            downloadBlob(buildPdf(jpegBytes, output.width, output.height), 'pdf');
        } catch (error) {
            showFeedback('PDF oluşturulamadı.', 'error');
        }
    });

    editorModal.addEventListener('shown.bs.modal', () => {
        document.body.classList.add('diagram-modal-open');
        initializeTooltips(editorModal);
        canvas.focus({ preventScroll: true });
    });

    editorModal.addEventListener('hidden.bs.modal', () => {
        document.body.classList.remove('diagram-modal-open');
        dragState = null;
        labelDragState = null;
        regionLabelDragState = null;
        panState = null;
        edgeHandleState = null;
        freeArrowEndpointState = null;
        setArrowDropTarget('');
        nodeResizeState = null;
        pinchState = null;
        activeTouchPointers.clear();
        spacePanActive = false;
        canvas.classList.remove('is-panning', 'space-pan-active');
        disableConnectMode(false);
    });

    viewerModal.addEventListener('shown.bs.modal', () => {
        document.body.classList.add('diagram-modal-open');
        initializeTooltips(viewerModal);
    });

    viewerModal.addEventListener('hidden.bs.modal', () => {
        document.body.classList.remove('diagram-modal-open');
        hideViewerInfo();
    });

    document.addEventListener('keydown', (event) => {
        if (!editorModal.classList.contains('show')) return;
        const isFormField = event.target.matches('input, textarea, select');
        const modifier = event.ctrlKey || event.metaKey;
        if (event.code === 'Space' && !isFormField && !spacePanActive) {
            event.preventDefault();
            spacePanActive = true;
            applyViewport();
            return;
        }
        if (modifier && event.key.toLowerCase() === 'z' && !isFormField) {
            event.preventDefault();
            if (event.shiftKey) redoButton.click();
            else undoButton.click();
            return;
        }
        if (modifier && event.key.toLowerCase() === 'd' && !isFormField) {
            event.preventDefault();
            duplicateSelectedNode();
            return;
        }
        if (modifier && event.key.toLowerCase() === 'c' && !isFormField) {
            event.preventDefault();
            copySelection();
            return;
        }
        if (modifier && event.key.toLowerCase() === 'v' && !isFormField) {
            event.preventDefault();
            pasteSelection();
            return;
        }
        if (modifier && event.key.toLowerCase() === 'a' && !isFormField) {
            event.preventDefault();
            selected = null;
            selectedNodeIds = new Set(graph.nodes.map((node) => node.id));
            setStatus(`${selectedNodeIds.size} düğüm seçildi`);
            render();
            return;
        }
        if (modifier && ['+', '='].includes(event.key) && !isFormField) {
            event.preventDefault();
            zoomAt(viewState.zoom * 1.2);
            return;
        }
        if (modifier && event.key === '-' && !isFormField) {
            event.preventDefault();
            zoomAt(viewState.zoom / 1.2);
            return;
        }
        if ((event.key === 'Delete' || event.key === 'Backspace') && !isFormField && (selected || selectedNodeIds.size)) {
            event.preventDefault();
            deleteSelected();
            return;
        }
        if (!isFormField && selectedNodeIds.size && ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
            event.preventDefault();
            pushHistory();
            const amount = event.shiftKey ? 24 : 4;
            const deltaX = event.key === 'ArrowLeft' ? -amount : event.key === 'ArrowRight' ? amount : 0;
            const deltaY = event.key === 'ArrowUp' ? -amount : event.key === 'ArrowDown' ? amount : 0;
            selectedNodes().forEach((node) => {
                const dimensions = nodeDimensions(node);
                node.x = Math.min(WORLD_WIDTH - dimensions.halfWidth - 8, Math.max(dimensions.halfWidth + 8, node.x + deltaX));
                node.y = Math.min(WORLD_HEIGHT - dimensions.halfHeight - 8, Math.max(dimensions.halfHeight + 8, node.y + deltaY));
            });
            setStatus('Seçim taşındı');
            render();
            return;
        }
        if (event.key === 'Escape' && connectMode) {
            event.preventDefault();
            disableConnectMode();
            render();
        }
    });

    document.addEventListener('keyup', (event) => {
        if (event.code !== 'Space' || !spacePanActive) return;
        spacePanActive = false;
        applyViewport();
    });

    function openRequestedDiagramFromUrl() {
        const params = new URLSearchParams(window.location.search);
        const requestedId = params.get('edit_diagram') || '';
        const positionValue = Number.parseInt(params.get('diagram_position') || '', 10);
        if (!requestedId && !Number.isInteger(positionValue)) return;
        const textarea = document.querySelector('textarea[name="answer_text"], textarea[id$="answer_text"]');
        const markers = findDiagramMarkers(textarea) || [];
        let marker = requestedId
            ? markers.find((item) => item.graph.uid === requestedId)
            : null;
        if (!marker && Number.isInteger(positionValue) && positionValue >= 0) marker = markers[positionValue];
        if (!marker) return;

        const cleanUrl = new URL(window.location.href);
        cleanUrl.searchParams.delete('edit_diagram');
        cleanUrl.searchParams.delete('diagram_position');
        window.history.replaceState({}, '', `${cleanUrl.pathname}${cleanUrl.search}${cleanUrl.hash}`);
        textarea.setSelectionRange(marker.start, marker.end);
        window.requestAnimationFrame(() => openEditor(textarea, marker.encoded));
    }

    injectToolbarButtons();
    openRequestedDiagramFromUrl();
})();
