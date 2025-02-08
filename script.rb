najiz_data = [
  {contract: '1012863278', version: 1, nin: '1058852839'},
]

application = Domain::Contract::Applications::OutboundApplication.new(auth_context: Ejar3::Iam::AuthenticationService.system_user)
najiz_data.each do |obj|
  pp "Getting Data for #{obj[:contract]}"
  pp application.contract_details_v2(contract_number: obj[:contract], id_number: obj[:nin], major_version: obj[:version], minor_version: 0)
end
