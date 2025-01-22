{
    "projectName": "s3privateweb",
    "version": "3.1",
    "frontend": "javascript",
    "javascript": {
        "framework": "react",
        "config": {
            "SourceDir": "src",
            "DistributionDir": "build",
            "BuildCommand": "npm run-script build",
            "StartCommand": "npm run-script start"
        }
    },
    "providers": [
        "awscloudformation"
    ]
}