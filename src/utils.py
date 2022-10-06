def get_workflows():
    return {
        'amanda-wf-euw4-dev-001-image-width-resize': '99cc67e3906149598361cd8bb3fcffe1',
        'analysis-transcoder': 'b9172fc483204275b175d5768198fe5e'
    }

def get_workflow_by_name(workflow_name):
    return get_workflows()[workflow_name]

def get_workflow_details():
    return {
        'amanda-wf-euw4-dev-001-image-width-resize': {
            'id': '99cc67e3906149598361cd8bb3fcffe1',
            'filter': '*.png *.jpg *.jpeg'
        },
        'analysis-transcoder': {
            'id': 'b9172fc483204275b175d5768198fe5e',
            'filter': '*.mp4 *.mov'
        }
    }

def get_workflow_details_by_name(workflow_name):
    return get_workflow_details()[workflow_name]