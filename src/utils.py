def get_workflows():
    return {
        'amanda-wf-euw4-dev-001-image-width-resize': '99cc67e3906149598361cd8bb3fcffe1'
    }

def get_workflow_by_name(workflow_name):
    return get_workflows()[workflow_name]