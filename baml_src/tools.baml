class ShoeMileageQuery {
  intent "shoe_mileage"
  shoe_id int | null @description("Specific shoe ID, null for all shoes")
  active_only bool @description("Filter to only active (not retired) shoes")
}

class RunSummaryQuery {
  intent "run_summary"
  start_date string @description("Start date in YYYY-MM-DD format")
  end_date string @description("End date in YYYY-MM-DD format")
  with_dog bool @description("True for runs with Laika, False for solo")
}

function SelectTool(message: string) -> ShoeMileageQuery | RunSummaryQuery {
  client OllamaClient
  prompt #"
    Given a message about running data, extract the query parameters.

    {{ ctx.output_format }}

    {{ _.role("user") }} {{ message }}
  "#
}

test TestRunSummaryWithLaika {
  functions [SelectTool]
  args {
    message "How many miles did I run with Laika in September 2025?"
  }
}

test TestShoeMileage {
  functions [SelectTool]
  args {
    message "Show me mileage for all my active shoes"
  }
}

test TestSoloRuns {
  functions [SelectTool]
  args {
    message "Show me my solo runs from October 2025"
  }
}