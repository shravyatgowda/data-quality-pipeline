// Power Query (M) version of the same cleaning rules, for use inside Power BI.
// Replace the file path in Source with your own location of raw_events.csv.
let
    Source   = Csv.Document(File.Contents("C:\data\raw_events.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed    = Table.TransformColumnTypes(Promoted, {
                   {"event_id", Int64.Type}, {"event_time", type datetime},
                   {"spend", type number}, {"clicks", type number}}, "en-US"),
    Trimmed  = Table.TransformColumns(Typed, {{"channel", each Text.Lower(Text.Trim(_)), type text}}),
    NoDupes  = Table.Distinct(Trimmed, {"event_id"}),
    NoNulls  = Table.SelectRows(NoDupes, each [campaign] <> null and [campaign] <> "" and [event_time] <> null),
    ValidCh  = Table.SelectRows(NoNulls, each List.Contains({"email", "social", "search", "display"}, [channel])),
    NonNeg   = Table.SelectRows(ValidCh, each [spend] >= 0),
    Clicks   = Table.ReplaceValue(NonNeg, null, 0, Replacer.ReplaceValue, {"clicks"})
in
    Clicks
